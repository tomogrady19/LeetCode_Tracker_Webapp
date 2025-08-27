from fastapi import APIRouter, HTTPException
from models import LeetCodeStats
from services.leetcode import fetch_leetcode_stats

router = APIRouter(prefix="/api", tags=["API"])


# Get data
@router.get("/stats/{username}", response_model=LeetCodeStats)
async def get_leetcode_stats(username: str):
    username = username.strip()
    if username:
        return await fetch_leetcode_stats(username.strip())
    else:
        raise HTTPException(status_code=400, detail="No Username")


# Check backend is running
@router.get("/health")
async def health_check():
    return {"status": "healthy"}
