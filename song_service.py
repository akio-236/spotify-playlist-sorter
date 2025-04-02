import json
import os
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
from typing import List, Dict, Any, Set, Tuple
import os

logger = logging.getLogger("spotify_playlist_sorter")


class SongService:
    def __init__(self, spotify_client, data_dir: str = "data"):
        self.sp = spotify_client
        self.data_dir = data_dir

        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)

    def fetch_liked_songs(self):
        """Fetch all liked songs from Spotify."""
        liked_songs = []
        offset = 0
        limit = 50  # Fetch 50 songs at a time (Spotify's max limit)

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
        return liked_songs

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def fetch_artist_info(self, artist_id: str):
        """Fetch artist info with retry logic."""
        return self.sp.artist(artist_id)

    def fetch_song_metadata(
        self, liked_songs: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Fetch metadata (genres, artist, etc.) for each song."""
        song_data = []
        all_genres = set()

        logger.info("Fetching metadata for songs...")

        # Process songs in batches of 50 to avoid overwhelming the API
        for i in range(0, len(liked_songs), 50):
            batch = liked_songs[i : i + 50]
            for item in batch:
                track = item["track"]
                artist_id = track["artists"][0]["id"]

                try:
                    artist_info = self.fetch_artist_info(artist_id)
                    genres = artist_info.get("genres", [])
                    all_genres.update(genres)

                    song_data.append(
                        {
                            "name": track["name"],
                            "artist": track["artists"][0]["name"],
                            "genres": genres,
                            "uri": track["uri"],
                            "album": track["album"]["name"],
                            "album_image": track["album"]["images"][0]["url"]
                            if track["album"]["images"]
                            else None,
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Error fetching metadata for song '{track['name']}': {e}"
                    )

        logger.info("Fetched metadata for all songs.")
        return song_data, list(all_genres)

    def save_song_data(self, song_data: List[Dict[str, Any]], all_genres: List[str]):
        """Save song data to JSON files"""
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
        """Load song data from JSON files"""
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
