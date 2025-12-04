from typing import Optional

from pydantic import BaseModel

from app.schemas.geo import Point


class PipeLineBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    medium: str
    diameter_mm: int
    centroid: Point
    description: Optional[str] = None


class PipeLineRead(PipeLineBase):
    id: int

    class Config:
        from_attributes = True


class PipeLineCreate(PipeLineBase):
    """Схема для создания нового трубопровода"""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Магистральный газопровод Уренгой-Помары-Ужгород",
                "owner": "Газпром Трансгаз Самара",
                "year_commissioned": 1985,
                "medium": "gas",
                "diameter_mm": 720,
                "centroid": {"lat": 53.405487, "lon": 50.288284},
                "description": "Описание трубопровода",
            }
        }
