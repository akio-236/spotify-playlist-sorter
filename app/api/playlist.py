from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.services.auth_service import get_spotify_client
from app.services.playlist_service import (
    create_genre_playlists,
    create_language_playlists,
    get_user_playlists,
    delete_playlist,
)

router = APIRouter()


class PlaylistInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    public: bool
    image_url: Optional[str] = None
    tracks_count: int


@router.get("/", response_model=List[PlaylistInfo])
async def get_playlists():
    """
    Get all playlists created by the application
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        playlists = get_user_playlists(sp)
        return playlists

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get playlists: {str(e)}",
        )


@router.post("/genres", status_code=status.HTTP_201_CREATED)
async def generate_genre_playlists():
    """
    Create playlists organized by genre from liked songs
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        result = create_genre_playlists(sp)
        return {"message": "Genre playlists created successfully", "playlists": result}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create genre playlists: {str(e)}",
        )


@router.post("/languages", status_code=status.HTTP_201_CREATED)
async def generate_language_playlists():
    """
    Create playlists organized by language from liked songs
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        result = create_language_playlists(sp)
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
async def remove_playlist(playlist_id: str):
    """
    Remove a playlist by ID
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        deleted = delete_playlist(sp, playlist_id)
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
