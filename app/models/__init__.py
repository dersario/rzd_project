from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Импорты после определения Base для избежания циклических зависимостей
from app.models.object import Object, ObjectType  # noqa: E402

__all__ = ["Base", "Object", "ObjectType"]
