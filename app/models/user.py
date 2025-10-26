from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base
from app.services.snils import Snils


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    role: Mapped[str] = mapped_column(String(100))  # rail / road / pedestrian
    snils: Mapped[Optional[str]] = mapped_column(Snils, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(200))

    def set_snils(self, snils_str: str) -> None:
        """Установка СНИЛС с валидацией""" 
        self.snils = Snils.create(snils_str)

    def get_snils_numeric(self) -> str:
        return Snils.clean_snils(self.snils) if self.snils else ""
