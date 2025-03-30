from venv import logger
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
import logging
import sys


def fetch_and_process_data(sp):
    """Fetch liked songs, metadata, and detect languages."""

    liked_songs = fetch_liked_songs(sp)

    song_data, all_genres = fetch_song_metadata(sp, liked_songs)

    language_data = detect_languages(song_data)

    save_data_to_json(song_data, all_genres, language_data)

    return song_data, language_data


def load_broad_genres():
    """Load the broad genres mapping from JSON."""
    try:
        with open("data/broad_genres.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(
            "Error: 'broad_genres.json' not found. Please ensure the file exists in the 'data' folder."
        )
        return None


def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Spotify Playlist Sorter.")

        # Authenticate with Spotify
        logger.info("Authenticating with Spotify...")
        sp = authenticate_spotify()

        # Fetch and process data
        logger.info("Fetching and processing data...")
        song_data, language_data = fetch_and_process_data(sp)

        # Load broad genres mapping
        logger.info("Loading broad genres mapping...")
        broad_genres = load_broad_genres()
        if broad_genres is None:
            sys.exit(1)  # Exit with error code

        # Organize songs by broad genre
        logger.info("Organizing songs by broad genre...")
        genre_playlists = organize_by_broad_genre(song_data, broad_genres)

        # Create playlists
        logger.info("Creating playlists...")
        create_playlists(sp, genre_playlists, language_data)

        logger.info("Spotify Playlist Sorter completed successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit with error code


if __name__ == "__main__":
    main()
