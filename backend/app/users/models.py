from pydantic import BaseModel, EmailStr
from sqlalchemy import String, Boolean, ForeignKey
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

class DbUserUpload(DbBase):
    __tablename__ = 'user_uploads'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    file_name: Mapped[str] = mapped_column(String(255), index=True)
    original_name: Mapped[str] = mapped_column(String(255), index=True)


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

class UserUpload(BaseModel):
    file_name: str
    original_name: str
    uploads_count: int
