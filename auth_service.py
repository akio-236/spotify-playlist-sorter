import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import HTTPException, Request
from app.core.config import get_settings
import logging

logger = logging.getLogger("spotify_playlist_sorter")


class SpotifyAuthService:
    def __init__(self):
        self.settings = get_settings()

    def get_auth_manager(self):
        """Get Spotify OAuth authentication manager"""
        return SpotifyOAuth(
            client_id=self.settings.SPOTIFY_CLIENT_ID,
            client_secret=self.settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=self.settings.SPOTIFY_REDIRECT_URI,
            scope=self.settings.SPOTIFY_SCOPE,
            cache_path=".cache",
        )

    def get_auth_url(self):
        """Get the Spotify authorization URL"""
        auth_manager = self.get_auth_manager()
        auth_url = auth_manager.get_authorize_url()
        return auth_url

    def get_access_token(self, code: str):
        """Get access token using authorization code"""
        auth_manager = self.get_auth_manager()
        try:
            token_info = auth_manager.get_access_token(code)
            return token_info
        except Exception as e:
            logger.error(f"Error getting access token: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid authorization code")

    def get_spotify_client(self, token=None):
        """Get authenticated Spotify client"""
        if token:
            # Use provided token
            return spotipy.Spotify(auth=token)
        else:
            # Use OAuth flow
            auth_manager = self.get_auth_manager()
            return spotipy.Spotify(auth_manager=auth_manager)

    def validate_token(self, request: Request):
        """Validate Spotify token from session or token storage"""
        auth_manager = self.get_auth_manager()

        if not auth_manager.validate_token(
            auth_manager.cache_handler.get_cached_token()
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired Spotify token. Please re-authenticate.",
            )

        return auth_manager.get_cached_token()
