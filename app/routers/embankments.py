from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.permissions import Authenticated
from app.schemas.embankment import EmbankmentCreate, EmbankmentRead
from app.services.object_service import ObjectService

router = APIRouter(prefix="/embankments", tags=["embankments"])


@router.get("/", response_model=list[EmbankmentRead])
def list_embankments(db: Session = Depends(get_db)):
    """Получить список всех насыпей"""
    service = ObjectService(db)
    return service.get_embankments()


@router.post(
    "/",
    response_model=EmbankmentRead,
    summary="Создать новую насыпь",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_embankment(embankment: EmbankmentCreate, db: Session = Depends(get_db)):
    """Создать новую насыпь"""
    service = ObjectService(db)
    return service.create_embankment(embankment)
