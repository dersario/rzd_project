from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Bridge(Base):
    __tablename__ = "bridges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    owner: Mapped[str] = mapped_column(String(200), index=True)
    year_commissioned: Mapped[int] = mapped_column(Integer, index=True)
    bridge_type: Mapped[str] = mapped_column(String(100))  # rail / road / pedestrian
    length_m: Mapped[int] = mapped_column(Integer)
    centroid_lat: Mapped[float] = mapped_column()
    centroid_lon: Mapped[float] = mapped_column()
