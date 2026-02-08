from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
from app.models.models import Athlete, Activity, AthleteMetrics, UCICategory, WeeklyRanking
from app.services.strava_service import strava_service


# UCI Categories definition
UCI_CATEGORIES = [
    UCICategory(code="elite", name="Elite", min_age=0, max_age=22),
    UCICategory(code="amateur", name="Amateur", min_age=23, max_age=29),
    UCICategory(code="master_a", name="Master A", min_age=30, max_age=39),
    UCICategory(code="master_b", name="Master B", min_age=40, max_age=49),
    UCICategory(code="master_c", name="Master C", min_age=50, max_age=59),
    UCICategory(code="master_d", name="Master D", min_age=60, max_age=None),
]


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
    def calculate_age(birthdate: Optional[datetime]) -> int:
        """Calculate age from birthdate."""
        if not birthdate:
            return 30  # Default age if not available
        
        today = datetime.now()
        age = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age
    
    @staticmethod
    def get_uci_category(age: int) -> str:
        """Determine UCI category based on age."""
        for category in UCI_CATEGORIES:
            if category.min_age <= age and (category.max_age is None or age <= category.max_age):
                return category.code
        return "amateur"  # Default
    
    @staticmethod
    def aggregate_metrics(athlete: Athlete, activities: list[Activity]) -> AthleteMetrics:
        """Aggregate weekly metrics for an athlete."""
        total_distance = sum(activity.distance for activity in activities)
        total_elevation = sum(activity.total_elevation_gain for activity in activities)
        longest_ride = max((activity.distance for activity in activities), default=0)
        
        # Calculate UCI category (for now using a default age calculation)
        # In a real scenario, we'd need birthdate from Strava
        age = 30  # Default age - Strava API might not always provide this
        uci_category = RankingService.get_uci_category(age)
        
        return AthleteMetrics(
            athlete=athlete,
            total_distance=total_distance,
            total_elevation=total_elevation,
            longest_ride=longest_ride,
            activities_count=len(activities),
            uci_category=uci_category
        )
    
    @staticmethod
    async def get_weekly_ranking(
        category: str = "general",
        gender: Optional[str] = None,
        week_offset: int = 0
    ) -> WeeklyRanking:
        """
        Get weekly ranking for a specific category and gender.
        
        Args:
            category: 'general', 'elite', 'amateur', 'master_a', 'master_b', 'master_c', 'master_d'
            gender: 'M', 'F', or None for all
            week_offset: 0 = current week, -1 = last week
        """
        week_start, week_end = RankingService.get_week_dates(week_offset)
        
        # Get club members
        members = await strava_service.get_club_members()
        
        # Get club activities for the week
        activities = await strava_service.get_club_activities(after=week_start, before=week_end)
        
        # Group activities by athlete
        activities_by_athlete = defaultdict(list)
        for activity in activities:
            activities_by_athlete[activity.athlete_id].append(activity)
        
        # Calculate metrics for each athlete
        athlete_metrics_list = []
        for member in members:
            # Filter by gender if specified
            if gender and member.sex != gender:
                continue
            
            member_activities = activities_by_athlete.get(member.id, [])
            
            # Skip athletes with no activities
            if not member_activities:
                continue
            
            metrics = RankingService.aggregate_metrics(member, member_activities)
            
            # Filter by category if not general
            if category != "general" and metrics.uci_category != category:
                continue
            
            athlete_metrics_list.append(metrics)
        
        # Sort by total distance (descending)
        athlete_metrics_list.sort(key=lambda x: x.total_distance, reverse=True)
        
        return WeeklyRanking(
            week_start=week_start,
            week_end=week_end,
            category=category,
            gender=gender,
            rankings=athlete_metrics_list
        )
    
    @staticmethod
    def get_categories() -> list[UCICategory]:
        """Get all available UCI categories."""
        return UCI_CATEGORIES


ranking_service = RankingService()
