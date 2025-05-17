from datetime import datetime
from typing import Optional

import msgspec

class UserBase(msgspec.Struct):
    """Base schema for user data."""
    name: str
    surname: str

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str

class UserUpdate(msgspec.Struct):
    """Schema for user update."""
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime
    updated_at: datetime

class UserList(msgspec.Struct):
    """Schema for list of users response."""
    items: list[UserResponse]
    total: int
