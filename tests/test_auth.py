import unittest
from unittest.mock import patch, Mock
import os
import json
from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import SpotifyAuthService


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Create a temporary cache file for testing
        self.test_cache = ".test_cache"
        if os.path.exists(self.test_cache):
            os.remove(self.test_cache)

    def tearDown(self):
        # Clean up the test cache file
        if os.path.exists(self.test_cache):
            os.remove(self.test_cache)

    @patch("app.api.auth.create_spotify_oauth")
    def test_login_endpoint(self, mock_create_oauth):
        # Mock the OAuth object
        mock_oauth = Mock()
        mock_oauth.get_authorize_url.return_value = (
            "https://accounts.spotify.com/authorize?client_id=test"
        )
        mock_create_oauth.return_value = mock_oauth

        # Test the login endpoint
        response = self.client.get("/login")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"auth_url": "https://accounts.spotify.com/authorize?client_id=test"},
        )
        mock_oauth.get_authorize_url.assert_called_once()

    @patch("app.api.auth.create_spotify_oauth")
    def test_callback_endpoint_success(self, mock_create_oauth):
        # Mock the OAuth object
        mock_oauth = Mock()
        token_info = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "test_refresh_token",
            "scope": "user-library-read",
        }
        mock_oauth.get_access_token.return_value = token_info
        mock_create_oauth.return_value = mock_oauth

        # Test the callback endpoint
        response = self.client.get("/callback?code=test_code")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), token_info)
        mock_oauth.get_access_token.assert_called_once_with("test_code")

    @patch("app.api.auth.create_spotify_oauth")
    def test_callback_endpoint_failure(self, mock_create_oauth):
        # Mock the OAuth object to raise an exception
        mock_oauth = Mock()
        mock_oauth.get_access_token.side_effect = Exception("Invalid code")
        mock_create_oauth.return_value = mock_oauth

        # Test the callback endpoint with an error
        response = self.client.get("/callback?code=invalid_code")

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Failed to get token", response.json()["detail"])

    @patch("app.api.auth.get_spotify_client")
    def test_current_user_endpoint(self, mock_get_client):
        # Mock the Spotify client
        mock_client = Mock()
        mock_client.current_user.return_value = {
            "id": "test_user",
            "display_name": "Test User",
        }
        mock_get_client.return_value = mock_client

        # Test the current_user endpoint
        response = self.client.get("/current-user")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"id": "test_user", "display_name": "Test User"}
        )
        mock_client.current_user.assert_called_once()

    @patch("app.api.auth.get_spotify_client")
    def test_current_user_not_authenticated(self, mock_get_client):
        # Mock no client (not authenticated)
        mock_get_client.return_value = None

        # Test the current_user endpoint when not authenticated
        response = self.client.get("/current-user")

        # Verify the response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    def test_logout_endpoint(self):
        # Create a mock cache file
        with open(self.test_cache, "w") as f:
            json.dump({"access_token": "test"}, f)

        # Mock the path to use our test cache
        with (
            patch("app.api.auth.os.path.exists", return_value=True),
            patch("app.api.auth.os.remove") as mock_remove,
        ):
            # Test the logout endpoint
            response = self.client.get("/logout")

            # Verify the response
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Successfully logged out"})
            mock_remove.assert_called_once()


if __name__ == "__main__":
    unittest.main()
