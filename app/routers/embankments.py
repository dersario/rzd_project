from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.embankment import Embankment
from app.schemas.embankment import EmbankmentRead
from app.services.mappers import embankment_to_read

router = APIRouter(prefix="/embankments", tags=["embankments"])


@router.get("/", response_model=list[EmbankmentRead])
def list_embankments(db: Session = Depends(get_db)):
    models = db.execute(select(Embankment)).scalars().all()
    return [embankment_to_read(m) for m in models]
