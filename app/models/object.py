import json
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator

from app.models import Base


class JSONType(TypeDecorator):
    """Тип для хранения JSON данных"""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect) -> str | None:
        if value is not None:
            return json.dumps(value, ensure_ascii=False)
        return None

    def process_result_value(self, value: str | None, dialect) -> dict | None:
        if value is not None:
            return json.loads(value)
        return None


class ObjectType(str, Enum):
    """Тип объекта инфраструктуры"""

    BRIDGE = "bridge"
    EMBANKMENT = "embankment"
    PIPELINE = "pipeline"
    POWERLINE = "powerline"
    ITEM = "item"


class Object(Base):
    """Универсальная модель объекта инфраструктуры"""

    __tablename__ = "objects"

    # Общие поля
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    owner: Mapped[str] = mapped_column(String(200), index=True)
    type: Mapped[ObjectType] = mapped_column(String(50), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    year_commissioned: Mapped[int] = mapped_column(Integer, index=True)
    centroid_lat: Mapped[float] = mapped_column(Float)
    centroid_lon: Mapped[float] = mapped_column(Float)

    # Специфические данные в формате JSON
    specific_data: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONType, nullable=True
    )
