import httpx
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings
from app.models.models import Athlete, Activity


class StravaService:
    """Service for interacting with Strava API."""
    
    BASE_URL = "https://www.strava.com/api/v3"
    
    def __init__(self):
        self.access_token = settings.strava_access_token
        self.club_id = settings.strava_club_id
        
    def _get_headers(self) -> dict:
        """Get authorization headers for Strava API."""
        return {"Authorization": f"Bearer {self.access_token}"}
    
    async def get_club_members(self) -> list[Athlete]:
        """Get all members of the club."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/clubs/{self.club_id}/members",
                headers=self._get_headers(),
                params={"per_page": 200}
            )
            response.raise_for_status()
            members_data = response.json()
            
            return [
                Athlete(
                    id=member["id"],
                    firstname=member["firstname"],
                    lastname=member["lastname"],
                    sex=member.get("sex", "M"),
                    profile=member.get("profile"),
                    created_at=member.get("created_at"),
                    updated_at=member.get("updated_at")
                )
                for member in members_data
            ]
    
    async def get_athlete_activities(
        self, 
        athlete_id: int,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None
    ) -> list[Activity]:
        """Get activities for a specific athlete within a date range."""
        params = {
            "per_page": 200
        }
        
        if after:
            params["after"] = int(after.timestamp())
        if before:
            params["before"] = int(before.timestamp())
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/athletes/{athlete_id}/stats",
                    headers=self._get_headers(),
                    timeout=10.0
                )
                
                # For now, we'll use the activities endpoint
                # Note: This requires the athlete's own token, not club token
                # We'll need to adjust this based on available permissions
                
                # Fallback: get club activities
                response = await client.get(
                    f"{self.BASE_URL}/clubs/{self.club_id}/activities",
                    headers=self._get_headers(),
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                activities_data = response.json()
                
                # Filter by athlete
                athlete_activities = [
                    Activity(
                        id=activity["id"],
                        athlete_id=activity["athlete"]["id"],
                        name=activity["name"],
                        distance=activity.get("distance", 0),
                        total_elevation_gain=activity.get("total_elevation_gain", 0),
                        moving_time=activity.get("moving_time", 0),
                        start_date=datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00")),
                        type=activity.get("type", "Ride")
                    )
                    for activity in activities_data
                    if activity["athlete"]["id"] == athlete_id
                ]
                
                return athlete_activities
            except httpx.HTTPError:
                # Return empty list if we can't fetch activities
                return []
    
    async def get_club_activities(
        self,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None
    ) -> list[Activity]:
        """Get all club activities within a date range."""
        params = {"per_page": 200}
        
        if after:
            params["after"] = int(after.timestamp())
        if before:
            params["before"] = int(before.timestamp())
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/clubs/{self.club_id}/activities",
                    headers=self._get_headers(),
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                activities_data = response.json()
                
                return [
                    Activity(
                        id=activity["id"],
                        athlete_id=activity["athlete"]["id"],
                        name=activity["name"],
                        distance=activity.get("distance", 0),
                        total_elevation_gain=activity.get("total_elevation_gain", 0),
                        moving_time=activity.get("moving_time", 0),
                        start_date=datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00")),
                        type=activity.get("type", "Ride")
                    )
                    for activity in activities_data
                ]
            except httpx.HTTPError as e:
                print(f"Error fetching club activities: {e}")
                return []


strava_service = StravaService()
