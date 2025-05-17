from typing import AsyncGenerator

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# Load environment variables
load_dotenv()

# Database connection settings
DB_DRIVER = os.getenv("DB_DRIVER", "postgresql+asyncpg")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "user_db")

# Create database URL
DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables() -> None:
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables() -> None:
    """Drop database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)