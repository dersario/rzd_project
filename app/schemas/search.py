"""Схемы для поиска объектов"""

from typing import Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Схема запроса на поиск"""

    query: Optional[str] = Field(None, description="Текст для полнотекстового поиска")
    object_types: Optional[list[str]] = Field(
        None,
        description="Фильтр по типам объектов (bridge, embankment, pipeline, powerline, item)",
    )
    owners: Optional[list[str]] = Field(None, description="Фильтр по владельцам")
    year_from: Optional[int] = Field(None, description="Год ввода в эксплуатацию от")
    year_to: Optional[int] = Field(None, description="Год ввода в эксплуатацию до")
    limit: int = Field(20, ge=1, le=100, description="Количество результатов")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")


class SearchResultItem(BaseModel):
    """Элемент результата поиска"""

    id: int
    name: str
    owner: str
    type: str
    description: Optional[str]
    year_commissioned: int
    centroid: dict[str, float]
    specific_data: dict
    score: Optional[float] = None


class SearchResponse(BaseModel):
    """Ответ на запрос поиска"""

    total: int
    results: list[SearchResultItem]
