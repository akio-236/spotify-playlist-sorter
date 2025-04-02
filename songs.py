from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.services.auth_service import get_spotify_client
from app.services.song_service import (
    get_liked_songs,
    get_song_metadata_by_genre,
    get_song_metadata_by_language,
)

router = APIRouter()


class SongGenre(BaseModel):
    name: str
    count: int


class SongLanguage(BaseModel):
    name: str
    count: int


class SongItem(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    genres: List[str]
    uri: str
    image_url: Optional[str] = None
    preview_url: Optional[str] = None


@router.get("/liked", response_model=List[SongItem])
async def fetch_liked_songs(limit: int = 50, offset: int = 0):
    """
    Fetch user's liked songs with pagination
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        songs = get_liked_songs(sp, limit, offset)
        return songs

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch liked songs: {str(e)}",
        )


@router.get("/genres")
async def get_songs_by_genre():
    """
    Get song counts grouped by genre
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        genre_data = get_song_metadata_by_genre(sp)
        return genre_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch song genres: {str(e)}",
        )


@router.get("/languages")
async def get_songs_by_language():
    """
    Get song counts grouped by language
    """
    try:
        sp = get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        language_data = get_song_metadata_by_language(sp)
        return language_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch song languages: {str(e)}",
        )
