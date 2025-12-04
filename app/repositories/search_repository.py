"""Репозиторий для поиска объектов через SQLAlchemy"""

from typing import Any, Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.models.object import Object, ObjectType


class SearchRepository:
    """Репозиторий для поиска объектов через SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query: Optional[str] = None,
        object_types: Optional[list[str]] = None,
        owners: Optional[list[str]] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Поиск объектов в базе данных"""
        # Базовый запрос
        stmt = select(Object)

        # Условия фильтрации
        conditions = []

        # Полнотекстовый поиск по name, owner, description
        if query:
            search_pattern = f"%{query}%"
            conditions.append(
                or_(
                    Object.name.ilike(search_pattern),
                    Object.owner.ilike(search_pattern),
                    Object.description.ilike(search_pattern),
                )
            )

        # Фильтр по типам объектов
        if object_types:
            # Преобразуем строки в ObjectType enum
            type_enums = []
            for type_str in object_types:
                try:
                    type_enums.append(ObjectType(type_str))
                except ValueError:
                    continue  # Пропускаем неверные типы
            if type_enums:
                conditions.append(Object.type.in_(type_enums))

        # Фильтр по владельцам
        if owners:
            conditions.append(Object.owner.in_(owners))

        # Фильтр по году ввода в эксплуатацию
        if year_from is not None:
            conditions.append(Object.year_commissioned >= year_from)
        if year_to is not None:
            conditions.append(Object.year_commissioned <= year_to)

        # Применяем условия
        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Подсчет общего количества (для пагинации)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar() or 0

        # Применяем сортировку и пагинацию
        stmt = stmt.order_by(Object.id).limit(limit).offset(offset)

        # Выполняем запрос
        objects = list[Object](self.db.execute(stmt).scalars().all())

        # Форматирование результатов
        results = []
        for obj in objects:
            # Преобразуем объект в словарь
            result = {
                "id": obj.id,
                "name": obj.name,
                "owner": obj.owner,
                "type": obj.type,
                "description": obj.description,
                "year_commissioned": obj.year_commissioned,
                "centroid": {"lat": obj.centroid_lat, "lon": obj.centroid_lon},
                "specific_data": obj.specific_data or {},
            }
            results.append(result)

        return {
            "total": total,
            "results": results,
        }
