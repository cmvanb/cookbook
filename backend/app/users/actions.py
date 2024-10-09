from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.users.models import DbUser, UserCreate


def create_user(*, session: Session, params: UserCreate) -> DbUser:
    user = DbUser(
        email=params.email,
        hashed_password=get_password_hash(params.password),
        is_active=params.is_active,
        is_superuser=params.is_superuser,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def get_user_by_email(*, session: Session, email: str) -> DbUser | None:
    session_user = session.execute(
        select(DbUser).where(DbUser.email == email)
    ).scalar_one_or_none()

    return session_user
