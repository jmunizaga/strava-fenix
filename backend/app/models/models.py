from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Athlete(BaseModel):
    """Athlete model with basic information."""
    id: int
    firstname: str
    lastname: str
    sex: str  # 'M' or 'F'
    profile: Optional[str] = None  # Profile picture URL
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Activity(BaseModel):
    """Activity model with metrics."""
    id: int
    athlete_id: int
    name: str
    distance: float  # meters
    total_elevation_gain: float  # meters
    moving_time: int  # seconds
    start_date: datetime
    type: str


class UCICategory(BaseModel):
    """UCI category classification."""
    code: str
    name: str
    min_age: int
    max_age: Optional[int] = None


class AthleteMetrics(BaseModel):
    """Weekly metrics for an athlete."""
    athlete: Athlete
    total_distance: float  # meters
    total_elevation: float  # meters
    longest_ride: float  # meters
    activities_count: int
    uci_category: str


class WeeklyRanking(BaseModel):
    """Weekly ranking response."""
    week_start: datetime
    week_end: datetime
    category: str  # 'general', 'amateur', 'master_a', etc.
    gender: Optional[str] = None  # 'M', 'F', or None for all
    rankings: list[AthleteMetrics]
