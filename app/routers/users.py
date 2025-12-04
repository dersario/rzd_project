from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import (
    AuthenticatedAccount,
    AuthorizedAccount,
    create_token,
)
from app.db.session import get_db
from app.deps import Token
from app.permissions import Authenticated
from app.schemas.user import GetTokenSchema, RegisterUserSchema, UserSchema
from app.services.user_service import UserService

users_routers = APIRouter(prefix="/users", tags=["Пользватели"])


@users_routers.post("/get_token")
async def get_token(
    schema: GetTokenSchema, token: Token, session: Session = Depends(get_db)
):
    """Получить токен доступа"""
    service = UserService(session)
    user = service.authenticate(schema)
    access_token = await create_token(user.id, token)
    return access_token


@users_routers.post("")
async def register_user(
    schema: RegisterUserSchema,
    session: Session = Depends(get_db),
) -> UserSchema:
    """Зарегистрировать нового пользователя"""
    service = UserService(session)
    return service.register(schema)


@users_routers.get(
    "",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def get_my_data(me: AuthenticatedAccount):
    """Получить данные текущего пользователя"""
    return UserSchema.model_validate(me)


@users_routers.get("/{id}")
async def get_user_by_id(id: int, session: Session = Depends(get_db)) -> UserSchema:
    """Получить пользователя по ID"""
    service = UserService(session)
    return service.get_by_id(id)
