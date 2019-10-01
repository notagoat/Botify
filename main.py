import os
import sys

import spotipy
import spotipy.util as util
from mastodon import Mastodon


SPOTIFY = None


def get_spotify(username, scope):
    token = util.prompt_for_user_token(username, scope)
    return spotipy.Spotify(auth=token)


def get_songs(username, time_range="short_term", no_songs=10):
    """Get top songs in a time period from Spotify.

    Args:
        username (str): Spotify username.
        time_range (str): Either "short_term", "medium_term" or "long_term".
        no_songs (int): Number of songs to get for time period.
    Returns:
        (list): Each item is a dict which contains the song and artist keys.
            e.g. [{'song': song_name, 'artist': ['artist2', 'artist2']}]
    """

    songs = []
    results = SPOTIFY.current_user_top_tracks(
        time_range=time_range, limit=no_songs
    )
    for item in results['items']:
        songs.append(
            {'song': item["name"], 'artist': item['artists'], 'id': item['id']}
        )

    return songs


def feature_stats(data, feature):
    songs = [x[feature] for x in data]
    feature_avg = sum(songs) / len(songs)
    return min(songs), max(songs), feature_avg


def audio_features(song_ids):
    return SPOTIFY.audio_features(song_ids)


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

    # We grab token using prompts bcs its easier than tokens. you need to run
    # export SPOTIPY_CLIENT_ID=''
    # export SPOTIPY_CLIENT_SECRET=''
    scope = 'user-top-read'
    global SPOTIFY
    SPOTIFY = get_spotify(username, scope)

    time_ranges = ['short_term', 'medium_term', 'long_term']

    for time_range in time_ranges:
        songs = get_songs(username, time_range)

        features = audio_features([x['id'] for x in songs])

        # Text is formatted like the following
        # _Time Range_
        # Song // Artist |
        # ---
        # Feature avg: xx.xx%

        title = time_range.replace('_', ' ').title()
        toot_text = f'_{title}_\n'

        for song in songs:
            toot_text += f'{song["song"]} // {song["artist"][0]["name"]}\n'

        toot_text += '---\n'

        feature_names = ['danceability', 'speechiness', 'energy']
        for feature in feature_names:
            rating = feature_stats(features, feature)
            rating_perc = rating[1] * 100
            rating = f'{feature.title()} avg: {rating_perc:.2f}%'

            toot_text += f'{rating}\n'

        toot(toot_text)


if __name__ == '__main__':
    main()
