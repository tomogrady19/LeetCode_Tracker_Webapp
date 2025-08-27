from pydantic import BaseModel


# Helps to enforce types
class LeetCodeStats(BaseModel):
    username: str
    easy: int
    medium: int
    hard: int
    total: int
