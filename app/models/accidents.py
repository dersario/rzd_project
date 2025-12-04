from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Accident(Base):
    __tablename__ = "accidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    responsible: Mapped[str] = mapped_column(String(200), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    accident_type: Mapped[str] = mapped_column(String(100))  # rail / road / pedestrian
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    centroid_lat: Mapped[float] = mapped_column()
    centroid_lon: Mapped[float] = mapped_column()
