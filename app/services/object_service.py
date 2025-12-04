from typing import Any

from sqlalchemy.orm import Session

from app.models.object import Object, ObjectType
from app.repositories.object_repository import ObjectRepository
from app.schemas.bridge import BridgeCreate
from app.schemas.embankment import EmbankmentCreate
from app.schemas.item import ItemCreate
from app.schemas.pipeline import PipeLineCreate
from app.schemas.powerline import PowerLineCreate
from app.services.mappers import (
    bridge_to_read,
    embankment_to_read,
    pipeline_to_read,
    powerline_to_read,
)


class ObjectService:
    """Сервис для работы с объектами инфраструктуры"""

    def __init__(self, db: Session):
        self.repository = ObjectRepository(db)

    def get_bridges(self) -> list[dict[str, Any]]:
        """Получить список всех мостов"""
        objects = self.repository.get_by_type(ObjectType.BRIDGE)
        return [bridge_to_read(obj) for obj in objects]

    def create_bridge(self, bridge: BridgeCreate) -> dict[str, Any]:
        """Создать новый мост"""
        obj = Object(
            name=bridge.name,
            owner=bridge.owner,
            type=ObjectType.BRIDGE,
            year_commissioned=bridge.year_commissioned,
            centroid_lat=bridge.centroid.lat,
            centroid_lon=bridge.centroid.lon,
            specific_data={
                "bridge_type": bridge.bridge_type,
                "length_m": bridge.length_m,
            },
        )
        created = self.repository.create(obj)
        return bridge_to_read(created)

    def get_embankments(self) -> list[dict[str, Any]]:
        """Получить список всех насыпей"""
        objects = self.repository.get_by_type(ObjectType.EMBANKMENT)
        return [embankment_to_read(obj) for obj in objects]

    def create_embankment(self, embankment: EmbankmentCreate) -> dict[str, Any]:
        """Создать новую насыпь"""
        obj = Object(
            name=embankment.name,
            owner=embankment.owner,
            type=ObjectType.EMBANKMENT,
            year_commissioned=embankment.year_commissioned,
            centroid_lat=embankment.centroid.lat,
            centroid_lon=embankment.centroid.lon,
            specific_data={
                "type": embankment.type,
            },
        )
        created = self.repository.create(obj)
        return embankment_to_read(created)

    def get_pipelines(self) -> list[dict[str, Any]]:
        """Получить список всех трубопроводов"""
        objects = self.repository.get_by_type(ObjectType.PIPELINE)
        return [pipeline_to_read(obj) for obj in objects]

    def create_pipeline(self, pipeline: PipeLineCreate) -> dict[str, Any]:
        """Создать новый трубопровод"""
        obj = Object(
            name=pipeline.name,
            owner=pipeline.owner,
            type=ObjectType.PIPELINE,
            year_commissioned=pipeline.year_commissioned,
            centroid_lat=pipeline.centroid.lat,
            centroid_lon=pipeline.centroid.lon,
            specific_data={
                "medium": pipeline.medium,
                "diameter_mm": pipeline.diameter_mm,
            },
        )
        created = self.repository.create(obj)
        return pipeline_to_read(created)

    def get_powerlines(self) -> list[dict[str, Any]]:
        """Получить список всех ЛЭП"""
        objects = self.repository.get_by_type(ObjectType.POWERLINE)
        return [powerline_to_read(obj) for obj in objects]

    def create_powerline(self, powerline: PowerLineCreate) -> dict[str, Any]:
        """Создать новую ЛЭП"""
        obj = Object(
            name=powerline.name,
            owner=powerline.owner,
            type=ObjectType.POWERLINE,
            year_commissioned=powerline.year_commissioned,
            centroid_lat=powerline.centroid.lat,
            centroid_lon=powerline.centroid.lon,
            specific_data={
                "voltage_kv": powerline.voltage_kv,
            },
        )
        created = self.repository.create(obj)
        return powerline_to_read(created)

    def get_items(self) -> list[dict[str, Any]]:
        """Получить список всех элементов"""
        objects = self.repository.get_by_type(ObjectType.ITEM)
        return [
            {"id": obj.id, "name": obj.name, "description": obj.description}
            for obj in objects
        ]

    def create_item(self, item: ItemCreate) -> dict[str, Any]:
        """Создать новый элемент"""
        # Проверка на существование
        if self.repository.exists_by_name_and_type(item.name, ObjectType.ITEM):
            raise ValueError("Item with this name already exists")

        obj = Object(
            name=item.name,
            description=item.description,
            type=ObjectType.ITEM,
            owner="",  # Для Item owner не обязателен, но поле не nullable
            year_commissioned=0,  # Для Item year_commissioned не обязателен
            centroid_lat=0.0,  # Для Item координаты не обязательны
            centroid_lon=0.0,
        )
        created = self.repository.create(obj)
        return {
            "id": created.id,
            "name": created.name,
            "description": created.description,
        }

    def get_item_by_id(self, item_id: int) -> dict[str, Any]:
        """Получить элемент по ID"""
        obj = self.repository.get_by_id_and_type(item_id, ObjectType.ITEM)
        if obj is None:
            raise ValueError("Item not found")
        return {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
        }

    def delete_item(self, item_id: int) -> None:
        """Удалить элемент"""
        obj = self.repository.get_by_id_and_type(item_id, ObjectType.ITEM)
        if obj is None:
            raise ValueError("Item not found")
        self.repository.delete(obj)
