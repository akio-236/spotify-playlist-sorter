import logging
from backend.spotify_auth import authenticate_spotify
from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# delete all created playlists except liked songs
def delete_all_playlists_except_liked_songs(sp):
    """Delete all playlists except for Liked Songs."""
    user_id = sp.current_user()["id"]

    # Fetch all playlists
    playlists = []
    offset = 0
    limit = 50  # Max number of playlists per request

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        playlists.extend(results["items"])
        if len(results["items"]) < limit:
            break
        offset += limit

    logging.info(f"Fetched {len(playlists)} playlists.")

    # Delete playlists (except Liked Songs)
    for playlist in playlists:
        playlist_name = playlist["name"]
        playlist_id = playlist["id"]

        # Skip the "Liked Songs" collection (it's not a playlist)
        if playlist_name == "Liked Songs":
            logging.info(f"Skipping 'Liked Songs' (not a playlist).")
            continue

        # Delete the playlist
        sp.current_user_unfollow_playlist(playlist_id)
        logging.info(f"Deleted playlist: '{playlist_name}'.")

    logging.info("All playlists deleted except for Liked Songs.")


def main():
    """Main function to delete playlists."""
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Delete all playlists except Liked Songs
    delete_all_playlists_except_liked_songs(sp)


if __name__ == "__main__":
    main()
