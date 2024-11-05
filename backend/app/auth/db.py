from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.users.db import get_user_by_email
from app.users.models import DbUser

def authenticate(*, session: Session, email: str, password: str) -> DbUser | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None

    return user
