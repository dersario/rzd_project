from pydantic import BaseModel

from app.schemas.geo import LineString, Point


class PipeLineBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    medium: str
    diameter_mm: int
    centroid: Point
    geometry: LineString


class PipeLineRead(PipeLineBase):
    id: int

    class Config:
        from_attributes = True


