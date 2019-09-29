import sys

import mastodon
import spotipy
import spotipy.util as util
from mastodon import Mastodon


def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    songs = get_songs(username)

    for time_range in songs:
        toot_text = f'{time_range}\n'
        for song in songs[time_range]:
            toot_text += f'{song}\n'

        toot(toot_text)


def get_songs(username):
    #We grab token using prompts bcs its easier than tokens. you need to run
    # export SPOTIPY_CLIENT_ID=''
    # export SPOTIPY_CLIENT_SECRET=''


    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope) #We need a small ass scope

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        songs = {}
        ranges = ['short_term', 'medium_term', 'long_term'] #If you only want to post short / medium / long remove them from this list.
        for range in ranges:
            if not songs.get(range):
                songs[range] = []

            results = sp.current_user_top_tracks(time_range=range, limit=10) #We can change the limit easily
            for i, item in enumerate(results['items'], start=1):
                artist = item['artists'][0]['name']
                song_string = f'{i}: {item["name"]} // {artist}'
                songs[range].append(song_string)

    return songs


def toot(text):
    mastodon = Mastodon(
        access_token = "", #Enter Bot Access Token
        api_base_url = "", #Instance URL
    )

    mastodon.status_post(text) 


if __name__ == '__main__':
    main()
