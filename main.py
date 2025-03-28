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


def main():
    setup_logging()

    # Authenticate
    sp = authenticate_spotify()

    # Load mappings
    with open("language_mapping.json") as f:
        language_mapping = json.load(f)

    # Fetch and process data
    liked_songs = fetch_liked_songs(sp)
    song_data, all_genres = fetch_song_metadata(sp, liked_songs)
    language_data = detect_languages(song_data, language_mapping)
    save_data_to_json(all_genres, language_data)

    # Organize and create playlists
    with open("broad_genres.json") as f:
        broad_genres = json.load(f)

    genre_playlists = organize_by_broad_genre(song_data, broad_genres)
    create_playlists(sp, genre_playlists, language_data)


if __name__ == "__main__":
    main()
