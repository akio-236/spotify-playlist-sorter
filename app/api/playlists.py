from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Optional
from app.services.auth_service import SpotifyAuthService
from app.services.playlist_service import PlaylistService
from app.services.song_service import SongService

router = APIRouter()

# Instantiate the SpotifyAuthService
auth_service = SpotifyAuthService()


# Create a dependency to get the Spotify client
def get_spotify_client():
    return auth_service.get_spotify_client()


# Instantiate the SongService and PlaylistService using the Spotify client
def get_song_service(spotify_client=Depends(get_spotify_client)):
    return SongService(spotify_client)


def get_playlist_service(spotify_client=Depends(get_spotify_client)):
    return PlaylistService(spotify_client)


@router.post("/genres", status_code=status.HTTP_201_CREATED)
async def generate_genre_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
    song_service: SongService = Depends(get_song_service),
):
    """
    Create playlists organized by genre from liked songs
    """
    try:
        # Fetch liked songs
        liked_songs = song_service.fetch_liked_songs()

        # Group songs by genre
        genre_playlists = song_service.group_songs_by_genre(liked_songs)

        # Create genre playlists
        result = playlist_service.create_genre_playlists(genre_playlists)
        return {"message": "Genre playlists created successfully", "playlists": result}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create genre playlists: {str(e)}",
        )


@router.post("/languages", status_code=status.HTTP_201_CREATED)
async def generate_language_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
    song_service: SongService = Depends(get_song_service),
):
    """
    Create playlists organized by language from liked songs
    """
    try:
        # Fetch liked songs
        liked_songs = song_service.fetch_liked_songs()

        # Group songs by language
        language_playlists = song_service.group_songs_by_language(liked_songs)

        # Create language playlists
        result = playlist_service.create_language_playlists(language_playlists)
        return {
            "message": "Language playlists created successfully",
            "playlists": result,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create language playlists: {str(e)}",
        )
