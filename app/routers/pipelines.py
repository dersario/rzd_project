from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.models.pipeline import PipeLine
from app.permissions import Authenticated
from app.schemas.pipeline import PipeLineCreate, PipeLineRead
from app.services.mappers import pipeline_to_read

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.get("/", response_model=list[PipeLineRead])
def list_pipelines(db: Session = Depends(get_db)):
    models = db.execute(select(PipeLine)).scalars().all()
    return [pipeline_to_read(m) for m in models]


@router.post("/", response_model=PipeLineRead, summary="Создать новый трубопровод", dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_pipeline(pipeline: PipeLineCreate, db: Session = Depends(get_db)):
    db_pipeline = PipeLine(
        name=pipeline.name,
        owner=pipeline.owner,
        year_commissioned=pipeline.year_commissioned,
        medium=pipeline.medium,
        diameter_mm=pipeline.diameter_mm,
        centroid_lat=pipeline.centroid.lat,
        centroid_lon=pipeline.centroid.lon,
    )

    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)

    return pipeline_to_read(db_pipeline)
