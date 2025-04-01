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
    """Detect languages from songs using comprehensive language detection signals."""
    try:
        with open("data/language_mapping.json") as f:
            language_mapping = json.load(f)
    except FileNotFoundError:
        print("Error: 'language_mapping.json' not found.")
        return {}

    language_data = defaultdict(list)

    # Language indicators in artist names, song titles, and genres
    language_indicators = {
        "Korean": {
            "artists": [
                "korean",
                "bts",
                "blackpink",
                "twice",
                "exo",
                "nct",
                "stray kids",
                "ateez",
                "seventeen",
                "got7",
                "itzy",
                "aespa",
                "red velvet",
                "iu",
                "bigbang",
                "txt",
                "g-dragon",
                "shinee",
                "mamamoo",
                "monsta x",
                "gidle",
            ],
            "keywords": ["k-", "(k)", "한국", "hangul", "hangeul", "seoul"],
            "genres": ["k-pop", "k-rap", "k-rock", "k-ballad", "korean ost"],
        },
        "Japanese": {
            "artists": [
                "japanese",
                "babymetal",
                "one ok rock",
                "utada",
                "kyary",
                "perfume",
                "kenshi yonezu",
                "radwimps",
                "lisa",
                "ado",
                "king gnu",
                "yoasobi",
                "eve",
                "reol",
                "zutomayo",
                "malice mizer",
                "dir en grey",
                "gackt",
            ],
            "keywords": ["j-", "(j)", "日本", "tokyo", "osaka", "jpop", "jrock"],
            "genres": ["j-pop", "j-rock", "j-rap", "j-r&b", "japanese vgm", "anime"],
        },
        "Spanish": {
            "artists": [
                "latino",
                "spanish",
                "español",
                "bad bunny",
                "j balvin",
                "rosalía",
                "daddy yankee",
                "shakira",
                "enrique iglesias",
                "maluma",
                "karol g",
                "nicky jam",
                "luis fonsi",
                "ozuna",
                "anuel aa",
                "becky g",
                "rauw alejandro",
            ],
            "keywords": [
                "latin",
                "latino",
                "española",
                "español",
                "barcelona",
                "madrid",
                "mexico",
                "cuba",
            ],
            "genres": [
                "reggaeton",
                "latin pop",
                "latin hip hop",
                "spanish-language reggae",
                "bachata",
                "salsa",
                "flamenco",
                "spanish-language rock",
            ],
        },
        "Hindi": {
            "artists": [
                "hindi",
                "bollywood",
                "indian",
                "desi",
                "arijit singh",
                "neha kakkar",
                "badshah",
                "shreya ghoshal",
                "yo yo honey singh",
                "sonu nigam",
                "a.r. rahman",
                "kumar sanu",
                "alka yagnik",
                "lata mangeshkar",
                "kishore kumar",
            ],
            "keywords": ["hindi", "indian", "desi", "bollywood", "mumbai", "bhangra"],
            "genres": [
                "bollywood",
                "hindi pop",
                "hindi hip hop",
                "desi pop",
                "filmi",
                "bhangra",
            ],
        },
        "Chinese": {
            "artists": [
                "mandarin",
                "chinese",
                "cantopop",
                "cpop",
                "jay chou",
                "kris wu",
                "jackson wang",
                "lay zhang",
                "mayday",
                "jolin tsai",
                "g.e.m.",
                "eason chan",
                "joey yung",
                "jacky cheung",
                "taiwan",
                "hong kong",
            ],
            "keywords": [
                "c-pop",
                "mandarin",
                "cantonese",
                "中文",
                "beijing",
                "taiwan",
                "hong kong",
            ],
            "genres": [
                "c-pop",
                "mandopop",
                "cantopop",
                "chinese r&b",
                "chinese hip hop",
            ],
        },
        "French": {
            "artists": [
                "french",
                "français",
                "stromae",
                "indila",
                "maitre gims",
                "zaz",
                "aya nakamura",
                "christine and the queens",
                "angèle",
                "louane",
                "mylene farmer",
                "alizée",
                "pomme",
                "edith piaf",
                "daft punk",
            ],
            "keywords": [
                "français",
                "francais",
                "france",
                "paris",
                "chanson",
                "québec",
            ],
            "genres": [
                "french pop",
                "french jazz",
                "variété française",
                "french hip hop",
            ],
        },
        "Tamil": {
            "artists": [
                "tamil",
                "a.r. rahman",
                "yuvan shankar raja",
                "anirudh ravichander",
                "sid sriram",
                "ilayaraja",
                "harris jayaraj",
                "hipop tamizha",
            ],
            "keywords": ["tamil", "kollywood", "chennai", "madras"],
            "genres": ["kollywood", "tamil pop", "tamil hip hop", "tamil film music"],
        },
        "Arabic": {
            "artists": [
                "arabic",
                "arab",
                "amr diab",
                "fairuz",
                "nancy ajram",
                "elissa",
                "tamer hosny",
                "mohammed abdu",
                "umm kulthum",
                "kadim al sahir",
            ],
            "keywords": ["arabic", "arab", "العربية", "dubai", "cairo", "beirut"],
            "genres": ["arabic pop", "khaleeji", "raï", "arab folk"],
        },
        "German": {
            "artists": [
                "german",
                "deutsch",
                "rammstein",
                "kraftwerk",
                "tokio hotel",
                "nena",
                "falco",
                "scooter",
                "helene fischer",
            ],
            "keywords": ["german", "deutsch", "berlin", "hamburg", "munich"],
            "genres": [
                "german rock",
                "schlager",
                "german hip hop",
                "neue deutsche welle",
            ],
        },
        "Italian": {
            "artists": [
                "italian",
                "italiano",
                "laura pausini",
                "eros ramazzotti",
                "maneskin",
                "andrea bocelli",
                "zucchero",
                "tiziano ferro",
            ],
            "keywords": ["italian", "italiano", "roma", "milano", "napoli"],
            "genres": ["italian pop", "cantautore", "canzone napoletana"],
        },
    }

    # Add English as default with its own indicators
    language_indicators["English"] = {
        "artists": ["english", "american", "british", "australian", "canadian"],
        "keywords": ["uk", "usa", "london", "los angeles", "new york"],
        "genres": ["uk garage", "uk drill", "britpop", "uk hip hop", "americana"],
    }

    # Process each song
    for song in song_data:
        song_name = song["name"].lower()
        artist_name = song["artist"].lower()
        song_genres = [genre.lower() for genre in song["genres"]]
        language_found = False

        # First check: Check genre-based language signals from language_mapping.json
        for genre in song_genres:
            for lang, lang_genres in language_mapping.items():
                if genre in [g.lower() for g in lang_genres]:
                    language_data[lang].append(song["uri"])
                    language_found = True
                    break
            if language_found:
                break

        # Second check: Use the comprehensive language indicators
        if not language_found:
            for language, indicators in language_indicators.items():
                # Check artist name against language-specific artist indicators
                if any(artist in artist_name for artist in indicators["artists"]):
                    language_data[language].append(song["uri"])
                    language_found = True
                    break

                # Check song name and artist name against language keywords
                if any(
                    keyword in artist_name or keyword in song_name
                    for keyword in indicators["keywords"]
                ):
                    language_data[language].append(song["uri"])
                    language_found = True
                    break

                # Check genres against language-specific genre indicators (as a backup)
                if any(genre in song_genres for genre in indicators["genres"]):
                    language_data[language].append(song["uri"])
                    language_found = True
                    break

        # Last resort: If still not found, categorize as "English" (most common default)
        if not language_found:
            language_data["English"].append(song["uri"])

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
