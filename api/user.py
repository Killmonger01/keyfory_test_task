from typing import Annotated

from litestar import Controller, get, post, put, delete, Router
from litestar.di import Provide
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete, update as sql_update, func

from db.config import get_db
from db.models import User
from schemas.user import UserCreate, UserResponse, UserUpdate, UserList
from msgspec import to_builtins


class UserController(Controller):
    """User API controller."""

    path = "/users"
    tags = ["Users"]

    dependencies = {"db": Provide(get_db)}

    @post(status_code=HTTP_201_CREATED, description="Create a new user")
    async def create_user(self, data: UserCreate, db: AsyncSession) -> UserResponse:
        user = User(
            name=data.name,
            surname=data.surname,
            password=data.password,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return UserResponse(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @get(description="Get all users")
    async def get_users(
        self,
        db: AsyncSession,
        offset: Annotated[int, Parameter(ge=0, description="Skip N users")] = 0,
        limit: Annotated[int, Parameter(ge=1, le=100, description="Limit number of users")] = 100,
    ) -> UserList:
        result = await db.execute(select(User).offset(offset).limit(limit))
        users = result.scalars().all()

        total_result = await db.execute(select(func.count()).select_from(User))
        total = total_result.scalar() or 0

        return UserList(
            items=[
                UserResponse(
                    id=u.id,
                    name=u.name,
                    surname=u.surname,
                    created_at=u.created_at,
                    updated_at=u.updated_at,
                ) for u in users
            ],
            total=total,
        )

    @get("/{user_id:int}", description="Get a specific user by ID")
    async def get_user(
        self,
        db: AsyncSession,
        user_id: Annotated[int, Parameter(description="The user ID")]
    ) -> UserResponse:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")

        return UserResponse(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @put("/{user_id:int}", description="Update a user")
    async def update_user(
        self,
        db: AsyncSession,
        data: UserUpdate,
        user_id: Annotated[int, Parameter(description="The user ID")]
    ) -> UserResponse:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")

        update_data = {k: v for k, v in to_builtins(data).items() if v is not None}
        if update_data:
            update_stmt = (
                sql_update(User)
                .where(User.id == user_id)
                .values(**update_data)
                .returning(User)
            )
            updated_result = await db.execute(update_stmt)
            updated_user = updated_result.scalar_one()
            await db.commit()
        else:
            updated_user = user

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            surname=updated_user.surname,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )

    @delete("/{user_id:int}", status_code=HTTP_204_NO_CONTENT, description="Delete a user")
    async def delete_user(
        self,
        db: AsyncSession,
        user_id: Annotated[int, Parameter(description="The user ID")]
    ) -> None:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")

        await db.execute(sql_delete(User).where(User.id == user_id))
        await db.commit()


user_router = Router(path="/api", route_handlers=[UserController])
