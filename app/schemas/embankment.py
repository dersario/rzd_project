from typing import Optional

from pydantic import BaseModel

from app.schemas.geo import Point


class EmbankmentBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    type: str
    centroid: Point
    description: Optional[str] = None


class EmbankmentRead(EmbankmentBase):
    id: int

    class Config:
        from_attributes = True


class EmbankmentCreate(EmbankmentBase):
    """Схема для создания новой насыпи"""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Насыпь на участке Самара-Тольятти",
                "owner": "РЖД Поволжская",
                "year_commissioned": 1960,
                "type": "rail",
                "centroid": {"lat": 53.392693, "lon": 50.311848},
                "description": "Описание насыпи",
            }
        }
