from datetime import date

from pydantic import BaseModel

from app.schemas.geo import Point


class AccidentBase(BaseModel):
    responsible: str
    date: date
    accident_type: str
    centroid: Point


class AccidentRead(AccidentBase):
    id: int

    class Config:
        from_attributes = True


class AccidentCreate(AccidentBase):
    pass
