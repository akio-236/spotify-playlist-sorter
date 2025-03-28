import json
from spotify_auth import authenticate_spotify
from collections import defaultdict


def fetch_liked_songs(sp):
    """Fetch all liked songs from Spotify."""
    liked_songs = []
    offset = 0
    limit = 50  # Max number of songs per request

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        liked_songs.extend(results["items"])
        if len(results["items"]) < limit:
            break
        offset += limit

    print(f"Fetched {len(liked_songs)} liked songs.")
    return liked_songs


def fetch_song_metadata(sp, liked_songs):
    """Fetch metadata (genres, artist, etc.) for each song."""
    song_data = []
    all_genres = set()
    language_counter = defaultdict(int)

    for item in liked_songs:
        track = item["track"]
        artist_id = track["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        genres = artist_info["genres"]

        # Collect all unique genres
        all_genres.update(genres)

        song_data.append(
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "genres": genres,
                "uri": track["uri"],
            }
        )

    print("Fetched metadata for all songs.")
    return song_data, list(all_genres)


def detect_languages(song_data, language_mapping):
    """Detect languages from all songs (not just 'Other' playlist)"""
    language_data = defaultdict(list)

    for song in song_data:
        for genre in song["genres"]:
            for lang, lang_genres in language_mapping.items():
                if genre.lower() in [g.lower() for g in lang_genres]:
                    language_data[lang].append(song["uri"])
                    break
            else:
                language_data["Other Languages"].append(song["uri"])

    return language_data


def save_data_to_json(genres, language_data):
    """Save all data to JSON files"""
    with open("unique_genres.json", "w") as f:
        json.dump(genres, f, indent=4)
    with open("language_data.json", "w") as f:
        json.dump(language_data, f, indent=4)
    print("Data saved to JSON files.")


def main():
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Load mappings
    with open("language_mapping.json") as f:
        language_mapping = json.load(f)

    # Fetch data
    liked_songs = fetch_liked_songs(sp)
    song_data, all_genres = fetch_song_metadata(sp, liked_songs)
    language_data = detect_languages(song_data, language_mapping)

    # Save data
    save_data_to_json(all_genres, language_data)

    return song_data


if __name__ == "__main__":
    main()
