from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs, fetch_song_metadata
from organize_songs import organize_by_genre, create_playlists
from utils import setup_logging


def main():
    # Set up logging
    setup_logging()

    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Fetch liked songs
    liked_songs = fetch_liked_songs(sp)

    # Fetch song metadata
    song_data = fetch_song_metadata(sp, liked_songs)

    # Organize songs by genre
    genre_playlists = organize_by_genre(song_data)

    # Create playlists
    create_playlists(sp, genre_playlists)


if __name__ == "__main__":
    main()
