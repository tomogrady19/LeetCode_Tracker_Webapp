from datetime import datetime, timedelta
from typing import List
from sqlalchemy import func, desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from database import UserCheck
from models import LeaderboardEntry


async def record_user_check(db: AsyncSession, username: str, total_solved: int):
    """Record a user check in the database"""
    user_check = UserCheck(
        username=username,
        total_solved=total_solved,
        checked_at=datetime.utcnow()
    )
    db.add(user_check)
    await db.commit()
    await db.refresh(user_check)


async def get_leaderboard(db: AsyncSession) -> List[LeaderboardEntry]:
    """Get top 10 most checked users in the past week from database"""
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Use SQLAlchemy text() for raw SQL query
    query = text("""
        SELECT 
            username,
            COUNT(*) as check_count,
            MAX(total_solved) as latest_total_solved
        FROM user_checks 
        WHERE checked_at >= :week_ago 
        GROUP BY username 
        ORDER BY check_count DESC, latest_total_solved DESC 
        LIMIT 10
    """)

    result = await db.execute(query, {"week_ago": one_week_ago})
    rows = result.fetchall()

    leaderboard_data = [
        LeaderboardEntry(
            username=row.username,
            check_count=row.check_count,
            total_solved=row.latest_total_solved
        )
        for row in rows
    ]

    return leaderboard_data
