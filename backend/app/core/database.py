from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.models import Base
from app.users.actions import create_user, CreateUserParams
from app.users.models import DbUser

engine = create_engine(str(settings.DATABASE_PATH), echo=True)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_db)]

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        user = session.execute(
            select(DbUser).where(DbUser.email == settings.FIRST_SUPERUSER_EMAIL)
        ).scalar_one_or_none()

        if not user:
            user = create_user(
                session=session,
                params=CreateUserParams(
                    email=settings.FIRST_SUPERUSER_EMAIL,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                )
            )
