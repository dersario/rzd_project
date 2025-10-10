from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class PipeLine(Base):
    __tablename__ = "pipe_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    owner: Mapped[str] = mapped_column(String(200), index=True)
    year_commissioned: Mapped[int] = mapped_column(Integer, index=True)
    medium: Mapped[str] = mapped_column(String(50))  # oil / gas
    diameter_mm: Mapped[int] = mapped_column(Integer)
    geometry_geojson: Mapped[str] = mapped_column(Text)  # GeoJSON LineString
    centroid_lat: Mapped[float] = mapped_column()
    centroid_lon: Mapped[float] = mapped_column()


