from backend.spotify_auth import authenticate_spotify
from backend.fetch_songs import fetch_liked_songs, fetch_song_metadata
from backend.organize_songs import (
    organize_by_broad_genre,
    organize_other_playlist_by_language,
    create_playlists,
)
from backend.utils import setup_logging
import json


def main():
    # Set up logging
    setup_logging()

    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Fetch liked songs
    liked_songs = fetch_liked_songs(sp)

    # Fetch song metadata
    song_data = fetch_song_metadata(sp, liked_songs)

    # Load broad genres from JSON file
    with open("broad_genres.json", "r") as f:
        broad_genres = json.load(f)

    # Load language mapping from JSON file
    with open("language_mapping.json", "r") as f:
        language_mapping = json.load(f)

    # Organize songs by broad genre
    genre_playlists = organize_by_broad_genre(song_data, broad_genres)

    # Organize "Other" playlist by language
    other_songs = genre_playlists.get("Other", [])
    language_playlists = organize_other_playlist_by_language(
        sp, song_data, other_songs, language_mapping
    )

    # Create playlists
    create_playlists(sp, genre_playlists, language_playlists)


if __name__ == "__main__":
    main()
