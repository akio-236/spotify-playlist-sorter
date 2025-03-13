from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs, fetch_song_metadata
from organize_songs import organize_by_broad_genre, create_playlists
from utils import setup_logging
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

    # Organize songs by broad genre
    genre_playlists = organize_by_broad_genre(song_data, broad_genres)

    # Create playlists
    create_playlists(sp, genre_playlists)


if __name__ == "__main__":
    main()
