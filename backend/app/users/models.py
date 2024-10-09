from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


# Database layer
#-------------------------------------------------------------------------------

class DbUser(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)


# Transport layer
#-------------------------------------------------------------------------------

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

# API requests
class UserCreate(UserBase):
    password: str

class UserUpdateMe(BaseModel):
    email: EmailStr

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

# API responses
class UserPublic(UserBase):
    id: int

class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
