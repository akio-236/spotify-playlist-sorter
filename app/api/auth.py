from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
from app.services.auth_service import SpotifyAuthService

router = APIRouter()

# Instantiate the SpotifyAuthService
auth_service = SpotifyAuthService()


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None


@router.get("/login")
async def login():
    """
    Initiate the Spotify OAuth login flow
    """
    auth_url = auth_service.get_auth_url()
    return {"auth_url": auth_url}


@router.get("/callback")
async def callback(code: str, state: Optional[str] = None):
    """
    Handle the callback from Spotify OAuth
    """
    try:
        sp_oauth = auth_service.get_auth_manager()
        token_info = sp_oauth.get_access_token(code)

        # Save token info to cache file for future use
        with open(".cache", "w") as f:
            json.dump(token_info, f)

        return {"message": "Authentication successful", "token_info": token_info}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get token: {str(e)}",
        )


@router.get("/current-user")
async def get_current_user():
    """
    Get information about the current authenticated user
    """
    try:
        sp = auth_service.get_spotify_client()
        if not sp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        user_info = sp.current_user()
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
        )


@router.get("/logout")
async def logout():
    """
    Log out the current user by clearing the token cache
    """
    try:
        if os.path.exists(".cache"):
            os.remove(".cache")
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}",
        )
