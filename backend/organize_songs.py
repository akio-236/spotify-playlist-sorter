import json
import os
from collections import defaultdict
from spotify_auth import authenticate_spotify


def load_data_from_json():
    """Load all data from JSON files in data folder."""
    with open("data/broad_genres.json") as f:
        broad_genres = json.load(f)
    with open("data/song_data.json") as f:
        song_data = json.load(f)
    with open("data/language_data.json") as f:
        language_data = json.load(f)
    return broad_genres, song_data, language_data


def organize_by_broad_genre(song_data, broad_genres):
    """Organize songs into broad genre playlists."""
    genre_playlists = defaultdict(set)

    for song in song_data:
        for genre in song["genres"]:
            for bg, subgenres in broad_genres.items():
                if genre.lower() in [sg.lower() for sg in subgenres]:
                    genre_playlists[bg].add(song["uri"])
                    break

    return {k: list(v) for k, v in genre_playlists.items()}


def get_existing_playlist_tracks(sp, playlist_id):
    """Get existing tracks in a playlist."""
    tracks = set()
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        for item in results["items"]:
            tracks.add(item["track"]["uri"])
        if len(results["items"]) < limit:
            break
        offset += limit

    return tracks


def create_playlists(sp, genre_playlists, language_data):
    """Create all playlists (genres + languages)."""
    user_id = sp.current_user()["id"]

    # Create genre playlists
    for genre, uris in genre_playlists.items():
        # Check if playlist exists
        playlists = sp.current_user_playlists()
        playlist_exists = False
        for playlist in playlists["items"]:
            if playlist["name"] == f"{genre} Playlist":
                playlist_id = playlist["id"]
                playlist_exists = True
                break

        if not playlist_exists:
            playlist = sp.user_playlist_create(
                user=user_id, name=f"{genre} Playlist", public=True
            )
            playlist_id = playlist["id"]
            print(f"Created '{genre} Playlist'.")

        # Add only new songs
        existing_tracks = get_existing_playlist_tracks(sp, playlist_id)
        new_uris = [uri for uri in uris if uri not in existing_tracks]

        if new_uris:
            sp.playlist_add_items(playlist_id, new_uris)
            print(f"Added {len(new_uris)} songs to '{genre} Playlist'.")

    # Create language playlists
    for language, uris in language_data.items():
        # Check if playlist exists
        playlists = sp.current_user_playlists()
        playlist_exists = False
        for playlist in playlists["items"]:
            if playlist["name"] == f"{language} Playlist":
                playlist_id = playlist["id"]
                playlist_exists = True
                break

        if not playlist_exists:
            playlist = sp.user_playlist_create(
                user=user_id, name=f"{language} Playlist", public=True
            )
            playlist_id = playlist["id"]
            print(f"Created '{language} Playlist'.")

        # Add only new songs
        existing_tracks = get_existing_playlist_tracks(sp, playlist_id)
        new_uris = [uri for uri in uris if uri not in existing_tracks]

        if new_uris:
            sp.playlist_add_items(playlist_id, new_uris)
            print(f"Added {len(new_uris)} songs to '{language} Playlist'.")


def main():
    # Authenticate
    sp = authenticate_spotify()

    # Load data
    broad_genres, song_data, language_data = load_data_from_json()

    # Organize data
    genre_playlists = organize_by_broad_genre(song_data, broad_genres)

    # Create playlists
    create_playlists(sp, genre_playlists, language_data)


if __name__ == "__main__":
    main()
