from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.permissions import Authenticated
from app.schemas.pipeline import PipeLineCreate, PipeLineRead
from app.services.object_service import ObjectService

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.get("/", response_model=list[PipeLineRead])
def list_pipelines(db: Session = Depends(get_db)):
    """Получить список всех трубопроводов"""
    service = ObjectService(db)
    return service.get_pipelines()


@router.post(
    "/",
    response_model=PipeLineRead,
    summary="Создать новый трубопровод",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_pipeline(pipeline: PipeLineCreate, db: Session = Depends(get_db)):
    """Создать новый трубопровод"""
    service = ObjectService(db)
    return service.create_pipeline(pipeline)
