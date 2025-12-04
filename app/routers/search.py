"""Роутер для поиска объектов"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Поиск"])


@router.post("/objects", response_model=SearchResponse)
def search_objects(
    search_request: SearchRequest,
    db: Session = Depends(get_db),
):
    """Поиск объектов инфраструктуры через SQLAlchemy"""
    service = SearchService(db)
    return service.search(search_request)
