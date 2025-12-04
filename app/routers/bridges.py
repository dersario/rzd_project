from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import AuthorizedAccount
from app.db.session import get_db
from app.permissions import Authenticated
from app.schemas.bridge import BridgeCreate, BridgeRead
from app.services.object_service import ObjectService

router = APIRouter(prefix="/bridges", tags=["bridges"])


@router.get("/", response_model=list[BridgeRead])
def list_bridges(db: Session = Depends(get_db)):
    """Получить список всех мостов"""
    service = ObjectService(db)
    return service.get_bridges()


@router.post(
    "/",
    response_model=BridgeRead,
    summary="Создать новый мост",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def create_bridge(bridge: BridgeCreate, db: Session = Depends(get_db)):
    """Создать новый мост"""
    service = ObjectService(db)
    return service.create_bridge(bridge)
