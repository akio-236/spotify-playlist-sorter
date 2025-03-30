import json
import os
from spotify_auth import authenticate_spotify
from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_fixed

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)


def fetch_liked_songs(sp):
    """Fetch all liked songs from Spotify."""
    liked_songs = []
    offset = 0
    limit = 50  # Fetch 50 songs at a time (Spotify's max limit)

    while True:
        try:
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)
            liked_songs.extend(results["items"])
            if len(results["items"]) < limit:
                break
            offset += limit
        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            break

    print(f"Fetched {len(liked_songs)} liked songs.")
    return liked_songs


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def fetch_artist_info(sp, artist_id):
    """Fetch artist info with retry logic."""
    return sp.artist(artist_id)


def fetch_song_metadata(sp, liked_songs):
    """Fetch metadata (genres, artist, etc.) for each song."""
    song_data = []
    all_genres = set()

    # Process songs in batches of 50 to avoid overwhelming the API
    for i in range(0, len(liked_songs), 50):
        batch = liked_songs[i : i + 50]
        for item in batch:
            track = item["track"]
            artist_id = track["artists"][0]["id"]

            try:
                artist_info = fetch_artist_info(sp, artist_id)
                genres = artist_info.get("genres", [])
                all_genres.update(genres)

                song_data.append(
                    {
                        "name": track["name"],
                        "artist": track["artists"][0]["name"],
                        "genres": genres,
                        "uri": track["uri"],
                    }
                )
            except Exception as e:
                print(f"Error fetching metadata for song '{track['name']}': {e}")

    print("Fetched metadata for all songs.")
    return song_data, list(all_genres)


def detect_languages(song_data):
    """Detect languages from all songs using language mapping."""
    try:
        with open("data/language_mapping.json") as f:
            language_mapping = json.load(f)
    except FileNotFoundError:
        print(
            "Error: 'language_mapping.json' not found. Please ensure the file exists in the 'data' folder."
        )
        return {}

    language_data = defaultdict(list)

    for song in song_data:
        language_found = False
        for genre in song["genres"]:
            for lang, lang_genres in language_mapping.items():
                if genre.lower() in [g.lower() for g in lang_genres]:
                    language_data[lang].append(song["uri"])
                    language_found = True
                    break
            if language_found:
                break
        if not language_found:
            language_data["Other Languages"].append(song["uri"])

    return language_data


def save_data_to_json(song_data, all_genres, language_data):
    """Save all data to JSON files in data folder."""
    try:
        with open("data/unique_genres.json", "w") as f:
            json.dump(all_genres, f, indent=4)
        with open("data/language_data.json", "w") as f:
            json.dump(language_data, f, indent=4)
        with open("data/song_data.json", "w") as f:
            json.dump(song_data, f, indent=4)
        print("All data saved to data folder.")
    except Exception as e:
        print(f"Error saving data to JSON files: {e}")


def main():
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Increase timeout for spotipy client
    sp.requests_timeout = 30  # Set timeout to 30 seconds

    # Fetch data
    liked_songs = fetch_liked_songs(sp)
    song_data, all_genres = fetch_song_metadata(sp, liked_songs)
    language_data = detect_languages(song_data)

    # Save data
    save_data_to_json(song_data, all_genres, language_data)


if __name__ == "__main__":
    main()
