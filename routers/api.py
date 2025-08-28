from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import LeetCodeStats, LeaderboardResponse
from services.leetcode import fetch_leetcode_stats
from services.leaderboard import record_user_check, get_leaderboard
from database import get_db

router = APIRouter(prefix="/api", tags=["API"])


# Get data
@router.get("/stats/{username}", response_model=LeetCodeStats)
async def get_leetcode_stats(username: str, db: AsyncSession = Depends(get_db)):
    username = username.strip()
    if username:
        stats = await fetch_leetcode_stats(username.strip())
        # Record this check for the leaderboard
        await record_user_check(db, username, stats.total)
        return stats
    else:
        raise HTTPException(status_code=400, detail="No Username")


# Get leaderboard
@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard_data(db: AsyncSession = Depends(get_db)):
    entries = await get_leaderboard(db)
    return LeaderboardResponse(entries=entries)


# Check backend is running
@router.get("/health")
async def health_check():
    return {"status": "healthy"}