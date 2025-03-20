import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def authenticate_spotify():
    """Authenticate with Spotify and return a SpotifyOAuth object."""
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read playlist-modify-public",
    )
