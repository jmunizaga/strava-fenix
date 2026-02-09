from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
from app.models.models import Athlete, Activity, AthleteMetrics, WeeklyRanking
from app.services.strava_service import strava_service
from app.database import SessionLocal
from app.models.db_models import User
import time





class RankingService:
    """Service for calculating rankings and classifications."""
    
    @staticmethod
    def get_week_dates(week_offset: int = 0) -> tuple[datetime, datetime]:
        """
        Get the start and end dates for a week.
        week_offset: 0 = current week, -1 = last week, etc.
        Week runs from Monday to Sunday.
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # Get Monday of current week
        monday = today - timedelta(days=today.weekday())
        # Apply offset
        week_start = monday + timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return week_start, week_end
    

    
    @staticmethod
    def aggregate_metrics(athlete: Athlete, activities: list[Activity]) -> AthleteMetrics:
        """Aggregate weekly metrics for an athlete."""
        total_distance = sum(activity.distance for activity in activities)
        total_elevation = sum(activity.total_elevation_gain for activity in activities)
        longest_ride = max((activity.distance for activity in activities), default=0)
        
        return AthleteMetrics(
            athlete=athlete,
            total_distance=total_distance,
            total_elevation=total_elevation,
            longest_ride=longest_ride,
            activities_count=len(activities)
        )
    
    @staticmethod
    async def get_weekly_ranking(
        gender: Optional[str] = None,
        week_offset: int = -1
    ) -> WeeklyRanking:
        """
        Get weekly ranking for the specified gender.
        
        Args:
            gender: 'M', 'F', or None for all
            week_offset: 0 = current week, -1 = last week
        """
        week_start, week_end = RankingService.get_week_dates(week_offset)
        
        db = SessionLocal()
        try:
            # Get all registered users
            db_users = db.query(User).all()
            
            athlete_metrics_list = []
            
            for db_user in db_users:
                # Filter by gender if specified
                if gender and db_user.sex != gender:
                    continue
                
                # Check token expiration
                current_time = int(time.time())
                access_token = db_user.access_token
                
                if db_user.expires_at <= current_time + 300: # 5 mins buffer
                    print(f"Refreshing token for user {db_user.firstname}")
                    new_token_data = await strava_service.refresh_athlete_token(db_user.refresh_token)
                    if new_token_data:
                        access_token = new_token_data["access_token"]
                        db_user.access_token = access_token
                        db_user.refresh_token = new_token_data["refresh_token"]
                        db_user.expires_at = new_token_data["expires_at"]
                        db.commit()
                
                # Fetch activities for this user
                activities = await strava_service.get_athlete_activities(
                    athlete_id=db_user.id,
                    token=access_token,
                    after=week_start,
                    before=week_end
                )
                
                if not activities:
                    continue
                
                # Create Athlete model for metrics
                athlete = Athlete(
                    id=str(db_user.id),
                    firstname=db_user.firstname,
                    lastname=db_user.lastname,
                    sex=db_user.sex,
                    profile=db_user.profile
                )
                
                metrics = RankingService.aggregate_metrics(athlete, activities)
                
                athlete_metrics_list.append(metrics)
            
            # Sort by total distance (descending)
            athlete_metrics_list.sort(key=lambda x: x.total_distance, reverse=True)
            
            return WeeklyRanking(
                week_start=week_start,
                week_end=week_end,
                gender=gender,
                rankings=athlete_metrics_list
            )
        finally:
            db.close()
    



ranking_service = RankingService()
