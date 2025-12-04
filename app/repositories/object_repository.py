from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.object import Object, ObjectType
from app.repositories.base_repository import BaseRepository


class ObjectRepository(BaseRepository[Object]):
    """Репозиторий для работы с объектами инфраструктуры"""

    def __init__(self, db: Session):
        super().__init__(db, Object)

    def get_by_type(self, object_type: ObjectType) -> list[Object]:
        """Получить все объекты определенного типа"""
        return list(
            self.db.execute(select(Object).where(Object.type == object_type))
            .scalars()
            .all()
        )

    def get_by_id_and_type(self, id: int, object_type: ObjectType) -> Optional[Object]:
        """Получить объект по ID и типу"""
        obj = self.get_by_id(id)
        if obj and obj.type == object_type:
            return obj
        return None

    def exists_by_name_and_type(self, name: str, object_type: ObjectType) -> bool:
        """Проверить существование объекта по имени и типу"""
        result = self.db.execute(
            select(Object).where(Object.name == name, Object.type == object_type)
        ).scalar_one_or_none()
        return result is not None
