import logging
from typing import Dict, List, Set
import time

logger = logging.getLogger("spotify_playlist_sorter")


class PlaylistService:
    def __init__(self, spotify_client):
        self.sp = spotify_client

    def get_existing_playlist_tracks(self, playlist_id: str) -> Set[str]:
        """Get existing tracks in a playlist."""
        tracks = set()
        offset = 0
        limit = 100

        try:
            while True:
                results = self.sp.playlist_items(
                    playlist_id, offset=offset, limit=limit
                )

                # Add valid tracks to the set
                for item in results["items"]:
                    if item["track"] and "uri" in item["track"]:
                        tracks.add(item["track"]["uri"])

                if len(results["items"]) < limit:
                    break

                offset += limit

            return tracks
        except Exception as e:
            logger.error(f"Error getting playlist tracks: {str(e)}")
            return set()

    def add_tracks_in_batches(
        self, playlist_id: str, uris: List[str], batch_size: int = 100
    ):
        """Add tracks to playlist in batches to avoid API limits."""
        for i in range(0, len(uris), batch_size):
            batch = uris[i : i + batch_size]
            try:
                self.sp.playlist_add_items(playlist_id, batch)
                logger.info(f"Added batch of {len(batch)} songs to playlist.")
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error adding tracks: {str(e)}")

    def create_or_update_playlist(
        self, name: str, description: str, uris: List[str]
    ) -> str:
        """Create or update a playlist with the given name and add tracks."""
        if not uris:
            logger.warning(f"No tracks to add to playlist '{name}'")
            return None

        user_id = self.sp.current_user()["id"]

        # Check if playlist already exists
        playlists = self.sp.current_user_playlists()
        playlist_id = None

        for playlist in playlists["items"]:
            if playlist["name"] == name:
                playlist_id = playlist["id"]
                logger.info(f"Found existing playlist: {name}")
                break

        # Create playlist if it doesn't exist
        if not playlist_id:
            try:
                result = self.sp.user_playlist_create(
                    user=user_id, name=name, public=True, description=description
                )
                playlist_id = result["id"]
                logger.info(f"Created new playlist: {name}")
            except Exception as e:
                logger.error(f"Error creating playlist: {str(e)}")
                return None

        # Get existing tracks to avoid duplicates
        existing_tracks = self.get_existing_playlist_tracks(playlist_id)
        new_uris = [uri for uri in uris if uri not in existing_tracks]

        if new_uris:
            logger.info(f"Adding {len(new_uris)} new tracks to '{name}'")
            self.add_tracks_in_batches(playlist_id, new_uris)
        else:
            logger.info(f"No new tracks to add to '{name}'")

        return playlist_id

    def create_genre_playlists(
        self, genre_playlists: Dict[str, List[str]]
    ) -> Dict[str, Dict]:
        """Create playlists for each genre."""
        created_playlists = {}

        for genre, uris in genre_playlists.items():
            if not uris:  # Skip empty playlists
                continue

            name = f"{genre} Playlist"
            description = (
                f"Songs in the {genre} genre, organized by Spotify Playlist Sorter"
            )

            playlist_id = self.create_or_update_playlist(name, description, uris)

            if playlist_id:
                created_playlists[genre] = {
                    "id": playlist_id,
                    "name": name,
                    "track_count": len(uris),
                }

        return created_playlists

    def create_language_playlists(
        self, language_playlists: Dict[str, List[str]]
    ) -> Dict[str, Dict]:
        """Create playlists for each language."""
        created_playlists = {}

        for language, uris in language_playlists.items():
            if not uris:  # Skip empty playlists
                continue

            name = f"{language} Playlist"
            description = f"Songs in {language}, organized by Spotify Playlist Sorter"

            playlist_id = self.create_or_update_playlist(name, description, uris)

            if playlist_id:
                created_playlists[language] = {
                    "id": playlist_id,
                    "name": name,
                    "track_count": len(uris),
                }

        return created_playlists
