from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError

from app.auth.models import TokenPayload
from app.core import security
from app.core.config import settings
from app.core.db import SessionDep
from app.users.models import DbUser


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_PREFIX}/login/access-token'
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> DbUser:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, algorithms=[security.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials'
        )

    user = session.get(DbUser, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')

    return user

CurrentUserDep = Annotated[DbUser, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUserDep) -> DbUser:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='The user does not have superuser privileges',
        )

    return current_user
