import os
import uuid
from typing import Any
from PIL import Image

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, func

from app.auth.utils import CurrentUserDep, get_current_active_superuser
from app.core.config import settings
from app.core.db import SessionDep
from app.core.models import Message
from app.core.security import get_password_hash, verify_password
from app.users.db import (
    create_user, get_user_by_email, user_upload_file, user_delete_upload
)
from app.users.models import (
    DbUser, DbUserUpload, UserPublic, UsersPublic, UserCreate, UserRegister,
    UserUpdateMe, UserUpdatePassword, UserUpload,
)
from app.users.utils import validate_uploaded_image


# TODO: Password recovery.

router = APIRouter()


@router.post('/register', response_model=UserPublic)
def register(
    session: SessionDep,
    body: UserRegister,
) -> Any:
    user = get_user_by_email(session=session, email=body.email)

    if user:
        raise HTTPException(status_code=400, detail='Email is already registered')

    params=UserCreate(
        email=body.email,
        password=body.password,
        is_superuser=False,
    )
    user = create_user(session=session, params=params)
    return user


@router.get(
    '/',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(
    session: SessionDep,
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
def update_me(
    session: SessionDep,
    current_user: CurrentUserDep,
    body: UserUpdateMe,
) -> Any:
    if body.email:
        existing_user = get_user_by_email(session=session, email=body.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409,
                detail='User with this email already exists',
            )

    current_user.email = body.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.patch(
    '/me/password',
    response_model=Message,
)
def update_password(
    session: SessionDep,
    current_user: CurrentUserDep,
    body: UserUpdatePassword,
) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail='Incorrect password',
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400,
            detail='New password cannot be the same as the current password',
        )

    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password

    session.add(current_user)
    session.commit()

    return Message(message='Password updated successfully')


@router.post('/upload-image', response_model=UserUpload)
async def upload_image(
    session: SessionDep,
    current_user: CurrentUserDep,
    file: UploadFile,
):
    original_name = file.filename or ''

    uploads_count = session.query(DbUserUpload).filter(DbUserUpload.user_id == current_user.id).count()
    if uploads_count >= settings.USER_MAX_UPLOADS:
        raise HTTPException(
            status_code=400,
            detail='User has reached maximum number of uploads',
        )

    error = validate_uploaded_image(file)
    if error:
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    # TODO: Automatically scale down large images.

    uploads_count += 1
    file_name = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOADS_PATH, file_name)

    try:
        with open(file_path, 'wb') as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    upload = user_upload_file(
        session=session,
        user_id=current_user.id,
        file_name=file_name,
        original_name=original_name,
    )

    return UserUpload(
        file_name=upload.file_name,
        original_name=upload.original_name,
        uploads_count=uploads_count,
    )

@router.delete('/delete-image/{file_name}')
def delete_image(
    session: SessionDep,
    current_user: CurrentUserDep,
    file_name: str
):
    try:
        user_delete_upload(
            session=session,
            user_id=current_user.id,
            file_name=file_name,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail='Upload not found')

    file_path = os.path.join(settings.UPLOADS_PATH, file_name)

    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
