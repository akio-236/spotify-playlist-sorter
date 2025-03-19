import os

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")  # Read from environment variable
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")  # Read from environment variable
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")

# Other configurations
SCOPE = "user-library-read playlist-modify-public"
