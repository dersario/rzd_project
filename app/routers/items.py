from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.services.object_service import ObjectService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)):
    """Получить список всех элементов"""
    service = ObjectService(db)
    items = service.get_items()
    return [ItemRead(**item) for item in items]


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    """Создать новый элемент"""
    service = ObjectService(db)
    try:
        item = service.create_item(payload)
        return ItemRead(**item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Получить элемент по ID"""
    service = ObjectService(db)
    try:
        item = service.get_item_by_id(item_id)
        return ItemRead(**item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Удалить элемент"""
    service = ObjectService(db)
    try:
        service.delete_item(item_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
