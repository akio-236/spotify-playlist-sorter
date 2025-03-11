import json
import time
from spotify_auth import authenticate_spotify
from fetch_songs import fetch_liked_songs


def fetch_song_genres(sp, liked_songs):
    """
    Fetch unique genres from liked songs with rate limit handling.
    """
    unique_genres = set()  # To store unique genres

    for index, item in enumerate(liked_songs):
        track = item["track"]
        artist_id = track["artists"][0]["id"]

        try:
            # Fetch artist info (including genres)
            artist_info = sp.artist(artist_id)
            genres = artist_info["genres"]
            unique_genres.update(genres)  # Add genres to the set

            # Log progress every 100 songs
            if (index + 1) % 100 == 0:
                print(f"Processed {index + 1} songs out of {len(liked_songs)}.")

            # Add a small delay to avoid hitting the rate limit
            time.sleep(10)  # 1-second delay between requests

        except Exception as e:
            print(f"Error fetching genres for song {index + 1}: {e}")
            if "rate limit" in str(e).lower():
                # Extract the retry-after time from the error message
                retry_after = int(
                    e.headers.get("Retry-After", 10)
                )  # Default to 10 seconds
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)  # Wait before retrying
                continue
            else:
                continue

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
