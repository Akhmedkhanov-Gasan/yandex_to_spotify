import os
from yandex_music import Client as YandexClient
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def fetch_yandex_tracks(yandex_token):
    client = YandexClient(token=yandex_token)
    liked = client.users_likes_tracks().tracks
    ids = [t.id for t in liked]
    full_tracks = []
    for i in range(0, len(ids), 50):
        batch = ids[i:i+50]
        full_tracks.extend(client.tracks(batch))

    tracks = []
    for t in full_tracks:
        artists = ", ".join([artist.name for artist in t.artists])
        title = t.title
        tracks.append(f"{artists} - {title}")
    return tracks


def get_or_create_playlist(sp, user_id, name, description=None):
    playlists = sp.current_user_playlists(limit=50)
    for pl in playlists['items']:
        if pl['name'] == name and pl['owner']['id'] == user_id:
            return pl['id']
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False,
        description=description or "Synced from Yandex Music"
    )
    return playlist['id']


def get_playlist_track_uris(sp, playlist_id):
    uris = []
    results = sp.playlist_items(playlist_id, fields='items.track.uri,next', limit=100)
    while True:
        for item in results['items']:
            uris.append(item['track']['uri'])
        if results.get('next'):
            results = sp.next(results)
        else:
            break
    return set(uris)


def search_spotify_uris(sp, track_queries):
    uris = {}
    for q in track_queries:
        result = sp.search(q, type='track', limit=1)
        items = result.get('tracks', {}).get('items', [])
        if items:
            uri = items[0]['uri']
            uris[uri] = q
        else:
            print(f"Not found on Spotify: {q}")
    return uris


def add_tracks_to_playlist(sp, playlist_id, uris):
    items = list(uris)
    for i in range(0, len(items), 100):
        sp.playlist_add_items(playlist_id, items[i:i+100])


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    yandex_token = os.getenv('YANDEX_TOKEN')
    sp = Spotify(auth_manager=SpotifyOAuth(
        scope='playlist-modify-private playlist-read-private',
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
    ))
    user_id = sp.me()['id']

    playlist_name = "Yandex Music"
    playlist_id = get_or_create_playlist(sp, user_id, playlist_name)

    yandex_tracks = fetch_yandex_tracks(yandex_token)
    existing_uris = get_playlist_track_uris(sp, playlist_id)
    found_uris = search_spotify_uris(sp, yandex_tracks)
    new_uris = [uri for uri in found_uris if uri not in existing_uris]

    if new_uris:
        add_tracks_to_playlist(sp, playlist_id, new_uris)
        print(f"Added {len(new_uris)} new tracks to playlist '{playlist_name}'.")
    else:
        print(f"No new tracks found for playlist '{playlist_name}'.")
