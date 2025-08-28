from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime

# Database URL - SQLite file
DATABASE_URL = "sqlite+aiosqlite:///./leetcode_stats.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class UserCheck(Base):
    __tablename__ = "user_checks"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    total_solved = Column(Integer)
    checked_at = Column(DateTime, default=datetime.utcnow)


async def create_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency to get database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()