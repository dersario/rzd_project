from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.permissions import Authenticated
from app.schemas.powerline import PowerLineCreate, PowerLineRead
from app.services.object_service import ObjectService

router = APIRouter(prefix="/powerlines", tags=["powerlines"])


@router.get("/", response_model=list[PowerLineRead])
def list_powerlines(db: Session = Depends(get_db)):
    """Получить список всех ЛЭП"""
    service = ObjectService(db)
    return service.get_powerlines()


@router.post(
    "/",
    response_model=PowerLineRead,
    summary="Создать новую ЛЭП",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_powerline(
    powerline: PowerLineCreate,
    db: Session = Depends(get_db),
):
    """Создать новую ЛЭП"""
    service = ObjectService(db)
    return service.create_powerline(powerline)
