from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.powerline import PowerLine
from app.schemas.powerline import PowerLineCreate, PowerLineRead
from app.services.mappers import powerline_to_read

router = APIRouter(prefix="/powerlines", tags=["powerlines"])


@router.get("/", response_model=list[PowerLineRead])
def list_powerlines(db: Session = Depends(get_db)):
    models = db.execute(select(PowerLine)).scalars().all()
    return [powerline_to_read(m) for m in models]


@router.post("/", response_model=PowerLineRead, summary="Создать новую ЛЭП")
def create_powerline(powerline: PowerLineCreate, db: Session = Depends(get_db)):
    db_powerline = PowerLine(
        name=powerline.name,
        owner=powerline.owner,
        year_commissioned=powerline.year_commissioned,
        voltage_kv=powerline.voltage_kv,
        centroid_lat=powerline.centroid.lat,
        centroid_lon=powerline.centroid.lon,
    )

    db.add(db_powerline)
    db.commit()
    db.refresh(db_powerline)

    return powerline_to_read(db_powerline)
