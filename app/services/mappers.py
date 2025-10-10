import json
from typing import Any

from app.models.embankment import Embankment
from app.models.pipeline import PipeLine
from app.models.powerline import PowerLine


def powerline_to_read(model: PowerLine) -> dict[str, Any]:
    geom = json.loads(model.geometry_geojson)
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "voltage_kv": model.voltage_kv,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
        "geometry": {
            "coordinates": [
                {"lat": lat, "lon": lon} for lon, lat in geom.get("coordinates", [])
            ]
        },
    }


def pipeline_to_read(model: PipeLine) -> dict[str, Any]:
    geom = json.loads(model.geometry_geojson)
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "medium": model.medium,
        "diameter_mm": model.diameter_mm,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
        "geometry": {
            "coordinates": [
                {"lat": lat, "lon": lon} for lon, lat in geom.get("coordinates", [])
            ]
        },
    }


def embankment_to_read(model: Embankment) -> dict[str, Any]:
    geom = json.loads(model.geometry_geojson)
    ring = geom.get("coordinates", [[]])[0]
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "type": model.type,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
        "geometry": {"coordinates": [{"lat": lat, "lon": lon} for lon, lat in ring]},
    }
