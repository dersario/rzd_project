from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.permissions import Authenticated
from app.schemas.accidents import AccidentCreate, AccidentRead
from app.services.accident_service import AccidentService

router = APIRouter(prefix="/accident", tags=["Авария"])


@router.get("/", response_model=list[AccidentRead])
def list_accidents(db: Session = Depends(get_db)):
    """Получить список всех аварий"""
    service = AccidentService(db)
    return service.get_all()


@router.post(
    "/",
    response_model=AccidentRead,
    summary="Создать метку аварии",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_accident(accident: AccidentCreate, db: Session = Depends(get_db)):
    """Создать новую аварию"""
    service = AccidentService(db)
    return service.create(accident)
