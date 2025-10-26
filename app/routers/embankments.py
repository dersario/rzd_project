from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.models.embankment import Embankment
from app.permissions import Authenticated
from app.schemas.embankment import EmbankmentCreate, EmbankmentRead
from app.services.mappers import embankment_to_read

router = APIRouter(prefix="/embankments", tags=["embankments"])


@router.get("/", response_model=list[EmbankmentRead])
def list_embankments(db: Session = Depends(get_db)):
    models = db.execute(select(Embankment)).scalars().all()
    return [embankment_to_read(m) for m in models]


@router.post(
    "/",
    response_model=EmbankmentRead,
    summary="Создать новую насыпь",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_embankment(embankment: EmbankmentCreate, db: Session = Depends(get_db)):
    db_embankment = Embankment(
        name=embankment.name,
        owner=embankment.owner,
        year_commissioned=embankment.year_commissioned,
        type=embankment.type,
        centroid_lat=embankment.centroid.lat,
        centroid_lon=embankment.centroid.lon,
    )

    db.add(db_embankment)
    db.commit()
    db.refresh(db_embankment)

    return embankment_to_read(db_embankment)
