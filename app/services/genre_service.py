import json
import os
from collections import defaultdict
from typing import List, Dict, Any, Set
import logging

logger = logging.getLogger("spotify_playlist_sorter")


class GenreService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Load genre mapping
        self.genre_mapping = self._load_genre_mapping()

    def _load_genre_mapping(self):
        """Load genre mapping from JSON file or use default mapping"""
        mapping_file = os.path.join(self.data_dir, "broad_genres.json")

        try:
            with open(mapping_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(
                "Genre mapping file not found. Run broad_genres.py first or use default mapping."
            )
            # Return a minimal default mapping
            return {
                "Rock": ["rock", "alternative rock", "indie rock", "hard rock"],
                "Pop": ["pop", "dance pop", "electropop", "synthpop"],
                "Hip Hop": ["hip hop", "rap", "trap"],
                "Electronic": ["electronic", "edm", "house", "techno"],
                "R&B": ["r&b", "soul", "funk"],
                "Jazz": ["jazz", "smooth jazz"],
                "Classical": ["classical", "baroque"],
                "Metal": ["metal", "heavy metal"],
                "Other": [],
            }

    def organize_by_broad_genre(self, song_data: List[Dict[str, Any]]):
        """Organize songs into broad genre playlists, ensuring each song only goes into one playlist."""
        genre_playlists = defaultdict(list)
        processed_songs = set()  # Track which songs have been processed

        # Process genres in order of priority/specificity
        genre_priority = [
            "Classical",
            "Jazz",
            "Metal",
            "Punk",
            "Hip Hop",
            "R&B",
            "Blues",
            "Reggae",
            "Gospel",
            "Folk",
            "Country",
            "Latin",
            "World",
            "Electronic",
            "Rock",
            "Alternative",
            "Pop",
            "Soundtrack",
            "Holiday",
            "Children's",
            "Other",
        ]

        logger.info("Organizing songs by genre...")

        # First pass: assign songs to specific genres based on priority
        for priority_genre in genre_priority:
            for song in song_data:
                # Skip songs that are already assigned
                if song["uri"] in processed_songs:
                    continue

                for song_genre in song["genres"]:
                    if priority_genre in self.genre_mapping and song_genre.lower() in [
                        g.lower() for g in self.genre_mapping[priority_genre]
                    ]:
                        genre_playlists[priority_genre].append(song["uri"])
                        processed_songs.add(song["uri"])
                        break

        # Second pass: assign any remaining songs to "Other"
        for song in song_data:
            if song["uri"] not in processed_songs:
                genre_playlists["Other"].append(song["uri"])

        logger.info(
            f"Genre organization complete. Organized into {len(genre_playlists)} genre playlists."
        )
        return genre_playlists

    def save_genre_playlists(self, genre_playlists):
        """Save genre playlists to JSON file"""
        try:
            with open(os.path.join(self.data_dir, "genre_playlists.json"), "w") as f:
                json.dump(genre_playlists, f, indent=4)
            logger.info("Saved genre playlists to JSON file.")
        except Exception as e:
            logger.error(f"Error saving genre playlists: {e}")
            raise

    def load_genre_playlists(self):
        """Load genre playlists from JSON file"""
        try:
            with open(os.path.join(self.data_dir, "genre_playlists.json"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Genre playlists file not found.")
            return {}
        except Exception as e:
            logger.error(f"Error loading genre playlists: {e}")
            raise
