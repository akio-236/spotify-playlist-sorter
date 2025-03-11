import json
from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs


def fetch_song_genres(sp, liked_songs):
    """
    Fetch unique genres from liked songs.
    """
    unique_genres = set()  # To store unique genres

    for item in liked_songs:
        track = item["track"]
        artist_id = track["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        genres = artist_info["genres"]
        unique_genres.update(genres)  # Add genres to the set

    print(f"Found {len(unique_genres)} unique genres.")
    return list(unique_genres)  # Convert set to list for JSON serialization


def save_genres_to_json(genres, filename="unique_genres.json"):
    """
    Save unique genres to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(genres, f, indent=4)
    print(f"Genres saved to {filename}.")


def main():
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Fetch liked songs
    liked_songs = fetch_liked_songs(sp)

    # Fetch unique genres
    unique_genres = fetch_song_genres(sp, liked_songs)

    # Save genres to a JSON file
    save_genres_to_json(unique_genres)


if __name__ == "__main__":
    main()
