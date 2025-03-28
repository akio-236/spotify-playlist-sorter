import json
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

# Initialize Spotify client
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
)

# Language mapping (customize this as needed)
LANGUAGE_MAPPING = {
    "Hindi": ["bollywood", "hindi", "desi", "indian pop"],
    "Spanish": ["latin", "reggaeton", "spanish", "bachata"],
    "Korean": ["k-pop", "korean"],
    "Japanese": ["j-pop", "japanese", "anime"],
    "English": ["pop", "rock", "hip hop", "r&b"],  # Default for common genres
    "Other": [],  # Catch-all for unmapped languages
}


def fetch_all_liked_songs():
    """Fetch all liked songs with metadata."""
    print("Fetching liked songs...")
    songs = []
    offset = 0
    limit = 50  # Spotify's max per request

    while True:
        batch = sp.current_user_saved_tracks(limit=limit, offset=offset)
        for item in batch["items"]:
            track = item["track"]
            artist = sp.artist(track["artists"][0]["id"])  # Get artist details
            songs.append(
                {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "genres": artist["genres"],
                    "uri": track["uri"],
                    "language": None,  # To be determined later
                }
            )

        if len(batch["items"]) < limit:
            break
        offset += limit

    print(f"Fetched {len(songs)} songs.")
    return songs


def detect_languages(songs):
    """Detect language for each song based on genres."""
    print("Detecting languages...")
    language_data = defaultdict(int)

    for song in songs:
        detected = False
        for lang, keywords in LANGUAGE_MAPPING.items():
            if any(keyword in " ".join(song["genres"]).lower() for keyword in keywords):
                song["language"] = lang
                language_data[lang] += 1
                detected = True
                break

        if not detected:
            song["language"] = "Other"
            language_data["Other"] += 1

    return songs, dict(language_data)


def extract_unique_genres(songs):
    """Extract all unique genres from songs."""
    print("Extracting genres...")
    genres = set()
    for song in songs:
        genres.update(song["genres"])
    return sorted(genres)


def save_data(songs, language_data, genres):
    """Save all data to JSON files."""
    with open("liked_songs.json", "w") as f:
        json.dump(songs, f, indent=2)

    with open("language_data.json", "w") as f:
        json.dump(language_data, f, indent=2)

    with open("unique_genres.json", "w") as f:
        json.dump(genres, f, indent=2)

    print("Data saved to JSON files.")


def main():
    # Step 1: Fetch all liked songs with metadata
    songs = fetch_all_liked_songs()

    # Step 2: Detect languages
    songs_with_language, language_data = detect_languages(songs)

    # Step 3: Extract unique genres
    unique_genres = extract_unique_genres(songs)

    # Step 4: Save all data
    save_data(songs_with_language, language_data, unique_genres)


if __name__ == "__main__":
    main()
