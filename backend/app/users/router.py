from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func

from app.auth.utils import CurrentUser, get_current_active_superuser
from app.core.database import SessionDependency
from app.core.models import Message
from app.core.security import get_password_hash, verify_password
from app.users.actions import get_user_by_email
from app.users.models import (
    DbUser, UserPublic, UsersPublic, UserUpdateMe, UserUpdatePassword
)


router = APIRouter()

@router.get(
    '/',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(
    session: SessionDependency,
    skip: int = 0,
    limit: int = 100
) -> Any:
    count = session.query(func.count(DbUser.id)).scalar()

    statement = select(DbUser).offset(skip).limit(limit)
    users = list(session.execute(statement).scalars().all())

    data = [UserPublic.model_validate(user) for user in users]

    return UsersPublic(data=data, count=count)

@router.patch(
    '/me',
    response_model=UserPublic,
)
def update_user_me(
    session: SessionDependency,
    params: UserUpdateMe,
    current_user: CurrentUser,
) -> Any:
    if params.email:
        existing_user = get_user_by_email(session=session, email=params.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409,
                detail='User with this email already exists',
            )

    current_user.email = params.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

@router.patch(
    '/me/password',
    response_model=Message,
)
def update_user_password(
    session: SessionDependency,
    params: UserUpdatePassword,
    current_user: CurrentUser,
) -> Any:
    if not verify_password(params.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail='Incorrect password',
        )
    if params.current_password == params.new_password:
        raise HTTPException(
            status_code=400,
            detail='New password cannot be the same as the current password',
        )

    hashed_password = get_password_hash(params.new_password)
    current_user.hashed_password = hashed_password

    session.add(current_user)
    session.commit()

    return Message(message='Password updated successfully')
