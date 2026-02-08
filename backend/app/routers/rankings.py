from fastapi import APIRouter, Query
from typing import Optional
from app.models.models import WeeklyRanking, UCICategory
from app.services.ranking_service import ranking_service


router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get("/weekly", response_model=WeeklyRanking)
async def get_weekly_ranking(
    category: str = Query("general", description="Category: general, elite, amateur, master_a, master_b, master_c, master_d"),
    gender: Optional[str] = Query(None, description="Gender: M, F, or null for all"),
    week_offset: int = Query(0, description="Week offset: 0=current, -1=last week, etc.")
):
    """Get weekly ranking for the specified category and gender."""
    return await ranking_service.get_weekly_ranking(category, gender, week_offset)


@router.get("/categories", response_model=list[UCICategory])
async def get_categories():
    """Get all available UCI categories."""
    return ranking_service.get_categories()
