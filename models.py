from pydantic import BaseModel
from typing import List


# Helps to enforce types
class LeetCodeStats(BaseModel):
    username: str
    easy: int
    medium: int
    hard: int
    total: int


class LeaderboardEntry(BaseModel):
    username: str
    check_count: int
    total_solved: int


class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]
