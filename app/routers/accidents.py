from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.accidents import Accident
from app.schemas.accidents import AccidentCreate, AccidentRead
from app.services.mappers import accident_to_read

router = APIRouter(prefix="/accident", tags=["Авария"])


@router.get("/", response_model=list[AccidentRead])
def list_accidents(db: Session = Depends(get_db)):
    models = db.execute(select(Accident)).scalars().all()
    return [accident_to_read(m) for m in models]

@router.post("/", response_model=AccidentRead, summary="Создать метку аварии")
def create_accident(accident: AccidentCreate, db: Session = Depends(get_db)):
    db_accident = Accident(
        responsible=accident.responsible,
        date=accident.date,
        accident_type=accident.accident_type,
        centroid_lat=accident.centroid.lat,
        centroid_lon=accident.centroid.lon,
    )

    db.add(db_accident)
    db.commit()
    db.refresh(db_accident)

    return accident_to_read(db_accident)
