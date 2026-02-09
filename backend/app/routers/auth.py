from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
import os
from datetime import datetime
from ..database import get_db
from ..models.db_models import User
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login():
    """Redirects the user to Strava for authentication."""
    client_id = settings.strava_client_id
    # We use a placeholder redirect_uri that the frontend will handle or we proxy
    redirect_uri = "http://localhost:3000/callback" 
    scope = "read,read_all,profile:read_all,activity:read_all"
    
    strava_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"approval_prompt=force&"
        f"scope={scope}"
    )
    return {"url": strava_url}

@router.post("/callback")
async def callback(data: dict, db: Session = Depends(get_db)):
    """Handles the code exchange for tokens and saves the user."""
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.strava.com/api/v3/oauth/token",
            data={
                "client_id": settings.strava_client_id,
                "client_secret": settings.strava_client_secret,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
            
        token_data = response.json()
        athlete_data = token_data.get("athlete")
        
        # Save or update user
        user = db.query(User).filter(User.id == athlete_data["id"]).first()
        if not user:
            user = User(id=athlete_data["id"])
            db.add(user)
            
        user.firstname = athlete_data.get("firstname")
        user.lastname = athlete_data.get("lastname")
        user.profile = athlete_data.get("profile")
        user.sex = athlete_data.get("sex", "M")
        user.access_token = token_data["access_token"]
        user.refresh_token = token_data["refresh_token"]
        user.expires_at = token_data["expires_at"]
        
        db.commit()
        db.refresh(user)
        
        return {
            "status": "success",
            "athlete": {
                "firstname": user.firstname,
                "lastname": user.lastname,
                "profile": user.profile
            }
        }
