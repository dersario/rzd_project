from typing import Any

from app.models.accidents import Accident
from app.models.bridge import Bridge
from app.models.embankment import Embankment
from app.models.pipeline import PipeLine
from app.models.powerline import PowerLine


def powerline_to_read(model: PowerLine) -> dict[str, Any]:
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "voltage_kv": model.voltage_kv,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def pipeline_to_read(model: PipeLine) -> dict[str, Any]:
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "medium": model.medium,
        "diameter_mm": model.diameter_mm,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def embankment_to_read(model: Embankment) -> dict[str, Any]:
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "type": model.type,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def bridge_to_read(model: Bridge) -> dict[str, Any]:
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "bridge_type": model.bridge_type,
        "length_m": model.length_m,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def accident_to_read(model: Accident) -> dict[str, Any]:
    return {
        "id": model.id,
        "responsible": model.responsible,
        "date": model.date,
        "accident_type": model.accident_type,
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }
