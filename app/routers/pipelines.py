from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pipeline import PipeLine
from app.schemas.pipeline import PipeLineRead
from app.services.mappers import pipeline_to_read

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.get("/", response_model=list[PipeLineRead])
def list_pipelines(db: Session = Depends(get_db)):
    models = db.execute(select(PipeLine)).scalars().all()
    return [pipeline_to_read(m) for m in models]
