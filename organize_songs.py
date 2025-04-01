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
    """Organize songs into broad genre playlists, ensuring each song only goes into one playlist."""
    genre_playlists = defaultdict(list)
    processed_songs = set()  # Track which songs have been processed

    # Process genres in order of priority/specificity
    genre_priority = [
        "Classical",
        "Jazz",
        "Metal",
        "Punk",
        "Hip Hop",
        "R&B",
        "Blues",
        "Reggae",
        "Gospel",
        "Folk",
        "Country",
        "Latin",
        "World",
        "Electronic",
        "Rock",
        "Alternative",
        "Pop",
        "Soundtrack",
        "Holiday",
        "Children's",
        "Other",
    ]

    # First pass: assign songs to specific genres based on priority
    for priority_genre in genre_priority:
        for song in song_data:
            # Skip songs that are already assigned
            if song["uri"] in processed_songs:
                continue

            for song_genre in song["genres"]:
                if priority_genre in broad_genres and song_genre.lower() in [
                    g.lower() for g in broad_genres[priority_genre]
                ]:
                    genre_playlists[priority_genre].append(song["uri"])
                    processed_songs.add(song["uri"])
                    break

    # Second pass: assign any remaining songs to "Other"
    for song in song_data:
        if song["uri"] not in processed_songs:
            genre_playlists["Other"].append(song["uri"])

    return genre_playlists


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

    # Function to add tracks in batches
    def add_tracks_in_batches(playlist_id, uris, batch_size=100):
        """Add tracks to playlist in batches to avoid API limits."""
        for i in range(0, len(uris), batch_size):
            batch = uris[i : i + batch_size]
            sp.playlist_add_items(playlist_id, batch)
            print(f"Added batch of {len(batch)} songs to playlist.")

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
            add_tracks_in_batches(playlist_id, new_uris)
            print(f"Added total of {len(new_uris)} songs to '{genre} Playlist'.")

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
            add_tracks_in_batches(playlist_id, new_uris)
            print(f"Added total of {len(new_uris)} songs to '{language} Playlist'.")


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
