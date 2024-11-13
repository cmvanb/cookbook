from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.users.models import DbUser, DbUserUpload, UserCreate


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

def user_upload_file(*,
    session: Session,
    user_id: int,
    file_name: str,
    original_name: str
) -> DbUserUpload:
    upload = DbUserUpload(
        user_id=user_id,
        file_name=file_name,
        original_name=original_name,
    )

    session.add(upload)
    session.commit()
    session.refresh(upload)

    return upload

def user_delete_upload(*,
    session: Session,
    user_id: int,
    file_name: str
) -> None:
    upload = session.execute(
        select(DbUserUpload)
            .where(DbUserUpload.user_id == user_id)
            .where(DbUserUpload.file_name == file_name)
    ).scalar_one_or_none()

    if upload is None:
        raise KeyError('Upload not found')

    session.delete(upload)
    session.commit()
