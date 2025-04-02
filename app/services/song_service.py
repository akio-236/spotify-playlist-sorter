import json
import os
from typing import List, Dict, Any
import logging
import time
from spotipy.exceptions import SpotifyException

logger = logging.getLogger("spotify_playlist_sorter")

DATA_DIR = "data"
CACHE_FILE = os.path.join(DATA_DIR, "artist_cache.json")


class SongService:
    def __init__(self, spotify_client, data_dir: str = "data"):
        self.sp = spotify_client
        self.data_dir = data_dir

        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)

    def fetch_liked_songs(self, limit: int = 50, offset: int = 0) -> Dict:
        """Fetch all liked songs from Spotify."""
        if not isinstance(limit, int) or not isinstance(offset, int):
            raise ValueError("Limit and offset must be integers.")

        liked_songs = []
        logger.info("Fetching liked songs from Spotify...")

        while True:
            try:
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                liked_songs.extend(results["items"])

                if len(results["items"]) < limit:
                    break

                offset += limit
                logger.info(f"Fetched {len(liked_songs)} songs so far...")
            except Exception as e:
                logger.error(f"Error fetching liked songs: {e}")
                break

        logger.info(f"Fetched {len(liked_songs)} liked songs in total.")
        return {"items": liked_songs}

    def load_artist_cache() -> Dict:
        """Load artist cache from file."""
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading artist cache: {e}")
        return {}

    def save_artist_cache(cache: Dict):
        """Save artist cache to file."""
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f)
        except Exception as e:
            logger.error(f"Error saving artist cache: {e}")

    def group_songs_by_genre(self, liked_songs: Dict) -> Dict[str, List[str]]:
        """Group songs by genre."""
        genre_map = {}
        artist_ids = [
            item["track"]["artists"][0]["id"] for item in liked_songs["items"]
        ]  # Extract all artist IDs

        # Fetch artist info in batches of 50
        for i in range(0, len(artist_ids), 50):
            batch = artist_ids[i : i + 50]
            retries = 3  # Maximum number of retries
            while retries > 0:
                try:
                    artist_infos = self.sp.artists(batch)[
                        "artists"
                    ]  # Fetch info for multiple artists
                    for artist_info in artist_infos:
                        genres = artist_info.get("genres", [])
                        for genre in genres:
                            if genre not in genre_map:
                                genre_map[genre] = []
                            genre_map[genre].append(artist_info["uri"])
                    break  # Exit retry loop if successful
                except SpotifyException as e:
                    if e.http_status == 429:  # Rate limit exceeded
                        retry_after = int(
                            e.headers.get("Retry-After", 1)
                        )  # Default to 1 second
                        logger.warning(
                            f"Rate limit exceeded. Retrying after {retry_after} seconds..."
                        )
                        time.sleep(retry_after)
                        retries -= 1
                    else:
                        logger.error(f"Error fetching artist info: {e}")
                        break

            # Add a delay to avoid rate limiting
            time.sleep(1)

        logger.info(f"Grouped songs into {len(genre_map)} genres.")
        return genre_map

    def group_songs_by_language(self, liked_songs: Dict) -> Dict[str, List[str]]:
        """Group songs by language (placeholder implementation)."""
        # Placeholder: Implement logic to group songs by language
        # For now, return an empty dictionary
        logger.warning("Language grouping is not implemented yet.")
        return {}

    def save_song_data(self, song_data: List[Dict[str, Any]], all_genres: List[str]):
        """Save song data to JSON files."""
        try:
            with open(os.path.join(self.data_dir, "song_data.json"), "w") as f:
                json.dump(song_data, f, indent=4)

            with open(os.path.join(self.data_dir, "unique_genres.json"), "w") as f:
                json.dump(all_genres, f, indent=4)

            logger.info("Saved song data to JSON files.")
        except Exception as e:
            logger.error(f"Error saving song data: {e}")
            raise

    def load_song_data(self):
        """Load song data from JSON files."""
        try:
            with open(os.path.join(self.data_dir, "song_data.json"), "r") as f:
                song_data = json.load(f)

            with open(os.path.join(self.data_dir, "unique_genres.json"), "r") as f:
                all_genres = json.load(f)

            return song_data, all_genres
        except FileNotFoundError:
            logger.warning("Song data files not found. Need to fetch data first.")
            return [], []
        except Exception as e:
            logger.error(f"Error loading song data: {e}")
            raise
