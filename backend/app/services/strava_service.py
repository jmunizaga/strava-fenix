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
        
    def _get_headers(self, token: Optional[str] = None) -> dict:
        """Get authorization headers for Strava API."""
        used_token = token or self.access_token
        return {"Authorization": f"Bearer {used_token}"}
    
    async def refresh_athlete_token(self, refresh_token: str) -> dict:
        """Refresh a Strava access token."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://www.strava.com/api/v3/oauth/token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": settings.strava_client_secret,
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token"
                    }
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error refreshing token: {e}")
                return {}
    
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
            
            members = []
            for member in members_data:
                # Use name as ID if numeric ID is missing
                athlete_id = str(member.get("id")) if "id" in member else f"{member['firstname']}_{member['lastname']}"
                
                members.append(Athlete(
                    id=athlete_id,
                    firstname=member["firstname"],
                    lastname=member["lastname"],
                    sex=member.get("sex", "M"),
                    profile=member.get("profile"),
                    created_at=member.get("created_at"),
                    updated_at=member.get("updated_at")
                ))
            
            return members
    
    async def get_athlete_activities(
        self, 
        athlete_id: int,
        token: str,
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
                    f"{self.BASE_URL}/athlete/activities",
                    headers=self._get_headers(token),
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                activities_data = response.json()
                
                athlete_activities = []
                for activity in activities_data:
                    # No need to filter by athlete_id as this endpoint returns activities for the authenticated athlete
                    if "id" not in activity:
                        continue

                    athlete_activities.append(Activity(
                        id=activity["id"],
                        athlete_id=str(athlete_id),
                        name=activity["name"],
                        distance=activity.get("distance", 0),
                        total_elevation_gain=activity.get("total_elevation_gain", 0),
                        moving_time=activity.get("moving_time", 0),
                        start_date=datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00")),
                        type=activity.get("type", "Ride")
                    ))
                
                return athlete_activities
            except Exception as e:
                print(f"Error fetching athlete activities for {athlete_id}: {e}")
                return []
    
    async def get_club_activities(
        self,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None
    ) -> list[Activity]:
        """Get all club activities within a date range."""
        params = {"per_page": 200}
        
        # Note: Strava Club API does NOT support 'after'/'before' params.
        # We must fetch the latest activities and filter manually.
        
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
                
                activities = []
                for activity in activities_data:
                    athlete_data = activity.get("athlete", {})
                    if not athlete_data:
                        continue
                        
                    start_date = datetime.fromisoformat(activity["start_date"].replace("Z", "+00:00"))
                    
                    # Manual filter by date
                    if after and start_date < after:
                        continue
                    if before and start_date > before:
                        continue

                    # Use name as ID if numeric ID is missing
                    athlete_id = str(athlete_data.get("id")) if "id" in athlete_data else f"{athlete_data['firstname']}_{athlete_data['lastname']}"
                    
                    if "id" not in activity:
                        continue
                        
                    activities.append(Activity(
                        id=activity["id"],
                        athlete_id=athlete_id,
                        name=activity["name"],
                        distance=activity.get("distance", 0),
                        total_elevation_gain=activity.get("total_elevation_gain", 0),
                        moving_time=activity.get("moving_time", 0),
                        start_date=start_date,
                        type=activity.get("type", "Ride")
                    ))
                
                return activities
            except httpx.HTTPError as e:
                print(f"Error fetching club activities: {e}")
                return []


strava_service = StravaService()
