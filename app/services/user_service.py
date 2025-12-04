from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import GetTokenSchema, RegisterUserSchema, UserSchema
from app.services.snils import Snils


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: int) -> UserSchema:
        """Получить пользователя по ID"""
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserSchema.model_validate(user)

    def authenticate(self, schema: GetTokenSchema) -> User:
        """Аутентификация пользователя"""
        user = self.repository.get_by_snils(schema.snils)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if user.password != schema.password:
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT, detail="Wrong password"
            )
        return user

    def register(self, schema: RegisterUserSchema) -> UserSchema:
        """Регистрация нового пользователя"""
        if not schema.snils or Snils.validate_snils(schema.snils):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный снилс"
            )

        if self.repository.exists_by_snils(schema.snils):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        user = User(
            name="user",
            role="user",
            snils=schema.snils,
            password=schema.password,
        )
        created = self.repository.create(user)
        return UserSchema.model_validate(created)
