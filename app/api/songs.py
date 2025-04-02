from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.services.auth_service import SpotifyAuthService  # Import the auth service
from app.services.song_service import SongService  # Import the song service

router = APIRouter()

# Instantiate the SpotifyAuthService
auth_service = SpotifyAuthService()


# Create a dependency to get the Spotify client
def get_spotify_client():
    return auth_service.get_spotify_client()


# Instantiate the SongService using the Spotify client
def get_song_service(spotify_client=Depends(get_spotify_client)):
    return SongService(spotify_client)


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
async def fetch_liked_songs(
    limit: int = 50,
    offset: int = 0,
    song_service: SongService = Depends(get_song_service),
):
    """
    Fetch user's liked songs with pagination
    """
    try:
        # Fetch liked songs using the SongService instance
        liked_songs = song_service.fetch_liked_songs()
        return [
            SongItem(
                id=song["track"]["id"],
                name=song["track"]["name"],
                artist=song["track"]["artists"][0]["name"],
                album=song["track"]["album"]["name"],
                genres=[],
                uri=song["track"]["uri"],
                image_url=song["track"]["album"]["images"][0]["url"]
                if song["track"]["album"]["images"]
                else None,
                preview_url=song["track"].get("preview_url"),
            )
            for song in liked_songs[offset : offset + limit]
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch liked songs: {str(e)}",
        )


@router.get("/genres")
async def get_songs_by_genre(song_service: SongService = Depends(get_song_service)):
    """
    Get song counts grouped by genre
    """
    try:
        # Fetch liked songs and their metadata
        liked_songs = song_service.fetch_liked_songs()
        song_data, all_genres = song_service.fetch_song_metadata(liked_songs)

        # Count songs per genre
        genre_counts = {}
        for song in song_data:
            for genre in song["genres"]:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return [
            {"name": genre, "count": count} for genre, count in genre_counts.items()
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch song genres: {str(e)}",
        )


@router.get("/languages")
async def get_songs_by_language(song_service: SongService = Depends(get_song_service)):
    """
    Get song counts grouped by language
    """
    try:
        # Placeholder for language grouping logic
        # You will need to implement this based on your requirements
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Language grouping is not implemented yet.",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch song languages: {str(e)}",
        )
