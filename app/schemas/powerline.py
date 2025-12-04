from typing import Optional

from pydantic import BaseModel

from app.schemas.geo import Point


class PowerLineBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    voltage_kv: int
    centroid: Point
    description: Optional[str] = None


class PowerLineRead(PowerLineBase):
    id: int

    class Config:
        from_attributes = True


class PowerLineCreate(PowerLineBase):
    """Схема для создания новой ЛЭП"""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "ВЛ 500кВ Самара-Тольятти",
                "owner": "СамараЭнерго",
                "year_commissioned": 1980,
                "voltage_kv": 500,
                "centroid": {"lat": 53.228661, "lon": 50.285445},
                "description": "Описание ЛЭП",
            }
        }
