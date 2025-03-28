from spotify_auth import authenticate_spotify
from fetch_songs import (
    fetch_liked_songs,
    fetch_song_metadata,
    detect_languages,
    save_data_to_json,
)
from organize_songs import organize_by_broad_genre, create_playlists
from utils import setup_logging
import json
import os


def main():
    # Set up logging
    setup_logging()

    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Fetch liked songs and metadata
    liked_songs = fetch_liked_songs(sp)
    song_data, all_genres = fetch_song_metadata(sp, liked_songs)

    # Detect languages (no need to pass language_mapping as it's loaded internally)
    language_data = detect_languages(song_data)

    # Save data to JSON files
    save_data_to_json(song_data, all_genres, language_data)

    # Load broad genres mapping
    with open("data/broad_genres.json", "r") as f:
        broad_genres = json.load(f)

    # Organize songs by broad genre
    genre_playlists = organize_by_broad_genre(song_data, broad_genres)

    # Create playlists
    create_playlists(sp, genre_playlists, language_data)


if __name__ == "__main__":
    main()
