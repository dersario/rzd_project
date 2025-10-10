from pydantic import BaseModel, Field


class Point(BaseModel):
    lat: float = Field(..., ge=51.0, le=55.5)
    lon: float = Field(..., ge=47.0, le=52.0)


class LineString(BaseModel):
    coordinates: list[Point]


class Polygon(BaseModel):
    coordinates: list[Point]


