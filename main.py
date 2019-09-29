import os
import sys

import spotipy
import spotipy.util as util
from mastodon import Mastodon


def get_songs(username, time_range="short_term", no_songs=10):
    """Get top songs in a time period from Spotify.

    Args:
        username (str): Spotify username.
        time_range (str): Either "short_term", "medium_term" or "long_term".
    Returns:
        (list): Each item is a dict which contains the song and artist keys.
            e.g. [{'song': song_name, 'artist': ['artist2', 'artist2']}]
    """

    # We grab token using prompts bcs its easier than tokens. you need to run
    # export SPOTIPY_CLIENT_ID=''
    # export SPOTIPY_CLIENT_SECRET=''


    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope) #We need a small ass scope

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        songs = []
        results = sp.current_user_top_tracks(
            time_range=time_range, limit=no_songs
        )
        for i, item in enumerate(results['items'], start=1):
            songs.append({'song': item["name"], 'artist': item['artists']})

    return songs


def toot(text):
    masto = Mastodon(
        access_token=os.getenv('MASTO_TOKEN'),
        api_base_url=os.getenv('MASTO_INSTANCE')
    )

    masto.status_post(text)


def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    time_ranges = ['short_term', 'medium_term', 'long_term']

    for time_range in time_ranges:
        songs = get_songs(username, time_range)

        toot_text = f'{time_range}\n'
        for song in songs:
            toot_text += f'{song["song"]} // {song["artist"][0]["name"]}\n'

        toot(toot_text)


if __name__ == '__main__':
    main()
