import json
import os
from collections import defaultdict
from typing import List, Dict, Any
import logging

logger = logging.getLogger("spotify_playlist_sorter")


class LanguageService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Load language mapping
        self.language_mapping = self._load_language_mapping()

    def _load_language_mapping(self):
        """Load language mapping from JSON file or use default mapping"""
        mapping_file = os.path.join(self.data_dir, "language_mapping.json")

        try:
            with open(mapping_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Language mapping file not found, using default mapping")
            # Default language mapping
            return {
                "Hindi": ["bollywood", "hindi pop", "hindi hip hop", "desi pop"],
                "Tamil": ["kollywood", "tamil pop", "tamil hip hop"],
                "Spanish": ["reggaeton", "latin", "spanish-language reggae"],
                "Korean": ["k-pop", "k-rap", "k-ballad"],
                "Japanese": ["j-pop", "j-rock", "j-rap"],
                "Chinese": ["c-pop", "mandopop", "chinese r&b"],
                "French": ["french jazz", "variété française"],
                "Other Languages": [],
            }

    def detect_languages(self, song_data: List[Dict[str, Any]]):
        """Detect languages from songs using comprehensive language detection signals."""
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
                "genres": [
                    "j-pop",
                    "j-rock",
                    "j-rap",
                    "j-r&b",
                    "japanese vgm",
                    "anime",
                ],
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
                "keywords": [
                    "hindi",
                    "indian",
                    "desi",
                    "bollywood",
                    "mumbai",
                    "bhangra",
                ],
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
                "genres": [
                    "kollywood",
                    "tamil pop",
                    "tamil hip hop",
                    "tamil film music",
                ],
            },
        }

        # Add English as default with its own indicators
        language_indicators["English"] = {
            "artists": ["english", "american", "british", "australian", "canadian"],
            "keywords": ["uk", "usa", "london", "los angeles", "new york"],
            "genres": ["uk garage", "uk drill", "britpop", "uk hip hop", "americana"],
        }

        logger.info("Detecting languages for songs...")

        # Process each song
        for song in song_data:
            song_name = song["name"].lower()
            artist_name = song["artist"].lower()
            song_genres = [genre.lower() for genre in song["genres"]]
            language_found = False

            # First check: Check genre-based language signals from language_mapping
            for genre in song_genres:
                for lang, lang_genres in self.language_mapping.items():
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

        logger.info(
            f"Language detection complete. Found tracks in {len(language_data)} languages."
        )
        return language_data

    def save_language_data(self, language_data):
        """Save language data to JSON file"""
        try:
            with open(os.path.join(self.data_dir, "language_data.json"), "w") as f:
                json.dump(language_data, f, indent=4)
            logger.info("Saved language data to JSON file.")
        except Exception as e:
            logger.error(f"Error saving language data: {e}")
            raise

    def load_language_data(self):
        """Load language data from JSON file"""
        try:
            with open(os.path.join(self.data_dir, "language_data.json"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Language data file not found.")
            return {}
        except Exception as e:
            logger.error(f"Error loading language data: {e}")
            raise
