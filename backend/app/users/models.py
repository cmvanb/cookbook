from pydantic import BaseModel, EmailStr
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import DbBase


# Database layer
#-------------------------------------------------------------------------------

class DbUser(DbBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)


# Transport layer
#-------------------------------------------------------------------------------

# Requests
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserUpdateMe(BaseModel):
    email: EmailStr

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

# Responses
class UserPublic(UserBase):
    id: int

class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
