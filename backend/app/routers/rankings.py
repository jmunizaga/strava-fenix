from fastapi import APIRouter, Query
from typing import Optional
from app.models.models import WeeklyRanking
from app.services.ranking_service import ranking_service


router = APIRouter(prefix="/rankings", tags=["rankings"])


@router.get("/weekly", response_model=WeeklyRanking)
async def get_weekly_ranking(
    gender: Optional[str] = Query(None, description="Gender: M, F, or null for all"),
    week_offset: int = Query(-1, description="Week offset: 0=current, -1=last week, etc.")
):
    """Get weekly ranking for the specified gender."""
    return await ranking_service.get_weekly_ranking(gender, week_offset)



