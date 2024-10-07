from datetime import timedelta

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.actions import authenticate
from app.auth.models import Token
from app.auth.utils import CurrentUser
from app.core.config import settings
from app.core.database import SessionDependency
from app.core.security import create_access_token
from app.users.models import UserPublic


router = APIRouter()

@router.post('/login/access-token')
def login_access_token(
    session: SessionDependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token)

@router.post('/login/test-token', response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    return current_user

# TODO: Password recovery.
