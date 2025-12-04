from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями"""

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_snils(self, snils: str) -> Optional[User]:
        """Получить пользователя по СНИЛС"""
        return self.db.execute(
            select(User).where(User.snils == snils)
        ).scalar_one_or_none()

    def exists_by_snils(self, snils: str) -> bool:
        """Проверить существование пользователя по СНИЛС"""
        result = self.get_by_snils(snils)
        return result is not None
