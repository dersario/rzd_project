from pydantic import BaseModel

from app.schemas.geo import Point, Polygon


class EmbankmentBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    type: str
    centroid: Point
    geometry: Polygon


class EmbankmentRead(EmbankmentBase):
    id: int

    class Config:
        from_attributes = True
