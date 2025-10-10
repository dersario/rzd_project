from pydantic import BaseModel

from app.schemas.geo import Point


class BridgeBase(BaseModel):
    name: str
    owner: str
    year_commissioned: int
    bridge_type: str
    length_m: int
    centroid: Point


class BridgeRead(BridgeBase):
    id: int

    class Config:
        from_attributes = True


class BridgeCreate(BridgeBase):
    pass
