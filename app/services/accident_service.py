from typing import Any

from sqlalchemy.orm import Session

from app.models.accidents import Accident
from app.repositories.accident_repository import AccidentRepository
from app.schemas.accidents import AccidentCreate
from app.services.mappers import accident_to_read


class AccidentService:
    """Сервис для работы с авариями"""

    def __init__(self, db: Session):
        self.repository = AccidentRepository(db)

    def get_all(self) -> list[dict[str, Any]]:
        """Получить список всех аварий"""
        accidents = self.repository.get_all()
        return [accident_to_read(accident) for accident in accidents]

    def create(self, accident: AccidentCreate) -> dict[str, Any]:
        """Создать новую аварию"""
        db_accident = Accident(
            responsible=accident.responsible,
            date=accident.date,
            accident_type=accident.accident_type,
            centroid_lat=accident.centroid.lat,
            centroid_lon=accident.centroid.lon,
        )
        created = self.repository.create(db_accident)
        return accident_to_read(created)
