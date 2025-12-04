from sqlalchemy.orm import Session

from app.models.accidents import Accident
from app.repositories.base_repository import BaseRepository


class AccidentRepository(BaseRepository[Accident]):
    """Репозиторий для работы с авариями"""

    def __init__(self, db: Session):
        super().__init__(db, Accident)
