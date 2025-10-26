from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import Token
from app.models.user import User
from app.permissions import BasePermission

SecuritySchema = HTTPBearer(auto_error=False)


async def create_access_token(
    data: dict, token_secret: Token, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_secret, algorithm="HS256")
    return encoded_jwt


async def create_token(id: int, token_secret: Token):
    token = await create_access_token({"id": id}, token_secret, timedelta(minutes=30))
    return token


async def authenticate_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(SecuritySchema)
    ],
    token_secret: Token,
    session: Session = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None
    token = credentials.credentials
    user_data = jwt.decode(token, token_secret, algorithms=["HS256"])
    user = session.execute(
        select(User).where(User.id == user_data["id"])
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user


AuthenticatedAccount = Annotated[User | None, Depends(authenticate_user)]


class AuthorizedAccount:
    def __init__(self, permission: BasePermission):
        self._permission = permission

    def __call__(self, account: AuthenticatedAccount):
        if not self._permission.check_permission(account):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
