import json
import random
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.embankment import Embankment
from app.models.pipeline import PipeLine
from app.models.powerline import PowerLine

SAMARA_BBOX = {
    "min_lat": 51.0,
    "max_lat": 55.5,
    "min_lon": 47.0,
    "max_lon": 52.0,
}


OWNERS = [
    "СамараЭнерго",
    "Газпром Трансгаз Самара",
    "Транснефть-Приволга",
    "РЖД Поволжская",
]


def _rand_lat() -> float:
    return round(random.uniform(SAMARA_BBOX["min_lat"], SAMARA_BBOX["max_lat"]), 6)


def _rand_lon() -> float:
    return round(random.uniform(SAMARA_BBOX["min_lon"], SAMARA_BBOX["max_lon"]), 6)


def _linestring_geojson(num_points: int = 5) -> str:
    coords = [[_rand_lon(), _rand_lat()] for _ in range(num_points)]
    return json.dumps({"type": "LineString", "coordinates": coords}, ensure_ascii=False)


def _polygon_geojson(size: float = 0.05) -> str:
    # simple square around a center point
    center_lat, center_lon = _rand_lat(), _rand_lon()
    half = size / 2
    ring = [
        [center_lon - half, center_lat - half],
        [center_lon - half, center_lat + half],
        [center_lon + half, center_lat + half],
        [center_lon + half, center_lat - half],
        [center_lon - half, center_lat - half],
    ]
    return json.dumps({"type": "Polygon", "coordinates": [ring]}, ensure_ascii=False)


def seed_all(
    db: Session, *, n_power: int = 10, n_pipe: int = 8, n_emb: int = 6
) -> None:
    if (
        db.query(PowerLine).first()
        or db.query(PipeLine).first()
        or db.query(Embankment).first()
    ):
        return

    random.seed(datetime.now().timestamp())

    # Power lines
    for i in range(1, n_power + 1):
        lat, lon = _rand_lat(), _rand_lon()
        db.add(
            PowerLine(
                name=f"ЛЭП-{i}",
                owner=random.choice(OWNERS),
                year_commissioned=random.randint(1970, 2022),
                voltage_kv=random.choice([35, 110, 220, 500]),
                geometry_geojson=_linestring_geojson(),
                centroid_lat=lat,
                centroid_lon=lon,
            )
        )

    # Pipelines
    for i in range(1, n_pipe + 1):
        lat, lon = _rand_lat(), _rand_lon()
        db.add(
            PipeLine(
                name=f"Трубопровод-{i}",
                owner=random.choice(OWNERS),
                year_commissioned=random.randint(1970, 2022),
                medium=random.choice(["oil", "gas"]),
                diameter_mm=random.choice([219, 325, 530, 720, 1020]),
                geometry_geojson=_linestring_geojson(),
                centroid_lat=lat,
                centroid_lon=lon,
            )
        )

    # Embankments
    for i in range(1, n_emb + 1):
        lat, lon = _rand_lat(), _rand_lon()
        db.add(
            Embankment(
                name=f"Насыпь-{i}",
                owner=random.choice(OWNERS),
                year_commissioned=random.randint(1950, 2020),
                type=random.choice(["rail", "road"]),
                geometry_geojson=_polygon_geojson(),
                centroid_lat=lat,
                centroid_lon=lon,
            )
        )

    db.commit()
