import os
import logging
from spotify_auth import authenticate_spotify
from utils import setup_logging


def delete_all_playlists(sp):
    """Delete all playlists created by the app"""
    playlists = sp.current_user_playlists()
    deleted_count = 0

    while playlists:
        for playlist in playlists["items"]:
            try:
                # Only delete playlists that match our naming pattern
                if playlist["name"].endswith("Playlist"):
                    sp.current_user_unfollow_playlist(playlist["id"])
                    logging.info(f"Deleted playlist: {playlist['name']}")
                    deleted_count += 1
            except Exception as e:
                logging.error(f"Error deleting {playlist['name']}: {str(e)}")

        if playlists["next"]:
            playlists = sp.next(playlists)
        else:
            playlists = None

    return deleted_count


def main():
    setup_logging()

    try:
        # Authenticate with Spotify
        sp = authenticate_spotify()

        # Delete playlists
        deleted = delete_all_playlists(sp)
        logging.info(f"Successfully deleted {deleted} playlists")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
