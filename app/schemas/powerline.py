from pydantic import BaseModel

from app.schemas.geo import LineString, Point


class PowerLineBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    voltage_kv: int
    centroid: Point
    geometry: LineString


class PowerLineRead(PowerLineBase):
    id: int

    class Config:
        from_attributes = True


