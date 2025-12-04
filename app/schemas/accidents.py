from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.schemas.geo import Point


class AccidentBase(BaseModel):
    responsible: str
    date: date
    accident_type: str
    centroid: Point
    description: Optional[str] = None


class AccidentRead(AccidentBase):
    id: int

    class Config:
        from_attributes = True


class AccidentCreate(AccidentBase):
    pass
