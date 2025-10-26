from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import (
    AuthenticatedAccount,
    AuthorizedAccount,
    create_token,
)
from app.db.session import get_db
from app.deps import Token
from app.models.user import User
from app.permissions import Authenticated
from app.schemas.user import GetTokenSchema, RegisterUserSchema, UserSchema

users_routers = APIRouter(prefix="/users", tags=["Пользватели"])


@users_routers.post("/get_token")
async def get_token(
    schema: GetTokenSchema, token: Token, session: Session = Depends(get_db)
):
    user = session.scalar(select(User).where(User.snils == schema.snils))
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    elif user.password != schema.password:
        raise HTTPException(status.HTTP_418_IM_A_TEAPOT, detail="Wrong password")
    token = await create_token(user.id, token)

    return token


@users_routers.post("")
async def register_user(
    schema: RegisterUserSchema,
    session: Session = Depends(get_db),
) -> UserSchema:
    if not schema.snils:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Неверный снилс")
    else:
        user = session.scalar(select(User).where(User.snils == schema.snils))
    if user is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = User(name="user", role="user", snils=schema.snils, password=schema.password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserSchema.model_validate(user)


@users_routers.get(
    "",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def get_my_data(me: AuthenticatedAccount):
    return UserSchema.model_validate(me)


@users_routers.get("/{id}")
async def get_user_by_id(id: int, session: Session = Depends(get_db)) -> UserSchema:
    user = session.get(User, id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserSchema.model_validate(user)
