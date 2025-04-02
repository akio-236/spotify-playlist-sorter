from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.services.auth_service import SpotifyAuthService  # Import the auth service
from app.services.playlist_service import PlaylistService  # Import the playlist service

router = APIRouter()

# Instantiate the SpotifyAuthService
auth_service = SpotifyAuthService()


# Create a dependency to get the Spotify client
def get_spotify_client():
    return auth_service.get_spotify_client()


# Instantiate the PlaylistService using the Spotify client
def get_playlist_service(spotify_client=Depends(get_spotify_client)):
    return PlaylistService(spotify_client)


class PlaylistInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    public: bool
    image_url: Optional[str] = None
    tracks_count: int


@router.get("/", response_model=List[PlaylistInfo])
async def get_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    """
    Get all playlists created by the application
    """
    try:
        playlists = playlist_service.sp.current_user_playlists()
        return [
            PlaylistInfo(
                id=playlist["id"],
                name=playlist["name"],
                description=playlist.get("description"),
                public=playlist["public"],
                image_url=playlist["images"][0]["url"] if playlist["images"] else None,
                tracks_count=playlist["tracks"]["total"],
            )
            for playlist in playlists["items"]
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get playlists: {str(e)}",
        )


@router.post("/genres", status_code=status.HTTP_201_CREATED)
async def generate_genre_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    """
    Create playlists organized by genre from liked songs
    """
    try:
        # Fetch liked songs
        liked_songs = playlist_service.sp.current_user_saved_tracks()
        genre_playlists = self.group_songs_by_genre(liked_songs)

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
):
    """
    Create playlists organized by language from liked songs
    """
    try:
        # Fetch liked songs
        liked_songs = playlist_service.sp.current_user_saved_tracks()
        language_playlists = self.group_songs_by_language(liked_songs)

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


@router.delete("/{playlist_id}", status_code=status.HTTP_200_OK)
async def remove_playlist(
    playlist_id: str, playlist_service: PlaylistService = Depends(get_playlist_service)
):
    """
    Remove a playlist by ID
    """
    try:
        deleted = playlist_service.sp.user_playlist_unfollow(
            user=playlist_service.sp.me()["id"], playlist_id=playlist_id
        )
        if deleted:
            return {"message": "Playlist deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found or couldn't be deleted",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete playlist: {str(e)}",
        )
