from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas import UserCreate

async def create_user(session: AsyncSession, user: UserCreate) -> User:
    db_user = User(**user.dict())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

async def update_user(session: AsyncSession, user_id: int, user: UserCreate) -> User | None:
    db_user = await get_user(session, user_id)
    if not db_user:
        return None
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    await session.commit()
    return db_user

async def delete_user(session: AsyncSession, user_id: int) -> bool:
    db_user = await get_user(session, user_id)
    if not db_user:
        return False
    await session.delete(db_user)
    await session.commit()
    return True
