from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.powerline import PowerLine
from app.schemas.powerline import PowerLineRead
from app.services.mappers import powerline_to_read

router = APIRouter(prefix="/powerlines", tags=["powerlines"])


@router.get("/", response_model=list[PowerLineRead])
def list_powerlines(db: Session = Depends(get_db)):
    models = db.execute(select(PowerLine)).scalars().all()
    return [powerline_to_read(m) for m in models]
