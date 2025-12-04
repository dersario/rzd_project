from typing import Generic, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Базовый репозиторий для работы с БД"""

    def __init__(self, db: Session, model: type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        """Получить объект по ID"""
        return self.db.get(self.model, id)

    def get_all(self) -> list[T]:
        """Получить все объекты"""
        return list(self.db.execute(select(self.model)).scalars().all())

    def create(self, obj: T) -> T:
        """Создать новый объект"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        """Обновить объект"""
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        """Удалить объект"""
        self.db.delete(obj)
        self.db.commit()
