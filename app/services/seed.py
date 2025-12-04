import random

from sqlalchemy.orm import Session

from app.models.object import Object, ObjectType
from app.repositories.object_repository import ObjectRepository

OWNERS = [
    "СамараЭнерго",
    "Газпром Трансгаз Самара",
    "Транснефть-Приволга",
    "РЖД Поволжская",
]


def seed_all(db: Session) -> None:
    repository = ObjectRepository(db)
    if repository.get_all():
        return

    # Предопределенные координаты
    bridges_data = [
        (53.388960, 50.319780),
        (53.432933, 50.180503),
        (53.433544, 50.117006),
        (53.433752, 50.115442),
    ]

    embankments_data = [
        (53.392693, 50.311848),
        (53.400803, 50.303161),
        (53.401123, 50.302899),
        (53.412280, 50.249981),
        (53.415327, 50.219042),
        (53.420585, 50.184330),
    ]

    powerlines_data = [
        (53.228661, 50.285445),
        (53.231564, 50.287240),
        (53.234900, 50.289239),
        (53.236998, 50.290605),
        (53.244703, 50.295111),
        (53.258239, 50.307644),
        (53.260358, 50.309411),
        (53.262078, 50.310946),
        (53.398558, 50.304464),
        (53.400224, 50.303558),
        (53.401891, 50.302233),
    ]

    pipelines_data = [
        (53.405487, 50.288284),
        (53.396522, 50.307507),
        (53.396522, 50.307507),
        (53.396522, 50.307507),
    ]

    # Мосты
    for i, (lat, lon) in enumerate(bridges_data, 1):
        obj = Object(
            name=f"Мост-{i}",
            owner=random.choice(OWNERS),
            type=ObjectType.BRIDGE,
            year_commissioned=random.randint(1960, 2020),
            centroid_lat=lat,
            centroid_lon=lon,
            specific_data={
                "bridge_type": random.choice(["rail", "road", "pedestrian"]),
                "length_m": random.randint(50, 500),
            },
        )
        repository.create(obj)

    # Насыпи
    for i, (lat, lon) in enumerate(embankments_data, 1):
        obj = Object(
            name=f"Насыпь-{i}",
            owner=random.choice(OWNERS),
            type=ObjectType.EMBANKMENT,
            year_commissioned=random.randint(1950, 2020),
            centroid_lat=lat,
            centroid_lon=lon,
            specific_data={
                "type": random.choice(["rail", "road"]),
            },
        )
        repository.create(obj)

    # ЛЭП
    for i, (lat, lon) in enumerate(powerlines_data, 1):
        obj = Object(
            name=f"ЛЭП-{i}",
            owner=random.choice(OWNERS),
            type=ObjectType.POWERLINE,
            year_commissioned=random.randint(1970, 2022),
            centroid_lat=lat,
            centroid_lon=lon,
            specific_data={
                "voltage_kv": random.choice([35, 110, 220, 500]),
            },
        )
        repository.create(obj)

    # Трубопроводы
    for i, (lat, lon) in enumerate(pipelines_data, 1):
        obj = Object(
            name=f"Трубопровод-{i}",
            owner=random.choice(OWNERS),
            type=ObjectType.PIPELINE,
            year_commissioned=random.randint(1970, 2022),
            centroid_lat=lat,
            centroid_lon=lon,
            specific_data={
                "medium": random.choice(["oil", "gas"]),
                "diameter_mm": random.choice([219, 325, 530, 720, 1020]),
            },
        )
        repository.create(obj)
