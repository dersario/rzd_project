"""Сервис для поиска объектов через SQLAlchemy"""

from sqlalchemy.orm import Session

from app.repositories.search_repository import SearchRepository
from app.schemas.search import SearchRequest, SearchResponse


class SearchService:
    """Сервис для поиска объектов"""

    def __init__(self, db: Session):
        self.search_repository = SearchRepository(db)

    def search(self, search_request: SearchRequest) -> SearchResponse:
        """Выполнить поиск объектов"""
        results = self.search_repository.search(
            query=search_request.query,
            object_types=search_request.object_types,
            owners=search_request.owners,
            year_from=search_request.year_from,
            year_to=search_request.year_to,
            limit=search_request.limit,
            offset=search_request.offset,
        )
        return SearchResponse(**results)
