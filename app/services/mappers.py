from typing import Any

from app.models.accidents import Accident
from app.models.object import Object


def powerline_to_read(model: Object) -> dict[str, Any]:
    specific_data = model.specific_data or {}
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "voltage_kv": specific_data.get("voltage_kv"),
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def pipeline_to_read(model: Object) -> dict[str, Any]:
    specific_data = model.specific_data or {}
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "medium": specific_data.get("medium"),
        "diameter_mm": specific_data.get("diameter_mm"),
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def embankment_to_read(model: Object) -> dict[str, Any]:
    specific_data = model.specific_data or {}
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "type": specific_data.get("type"),
        "centroid": {"lat": model.centroid_lat, "lon": model.centroid_lon},
    }


def bridge_to_read(model: Object) -> dict[str, Any]:
    specific_data = model.specific_data or {}
    return {
        "id": model.id,
        "name": model.name,
        "owner": model.owner,
        "year_commissioned": model.year_commissioned,
        "bridge_type": specific_data.get("bridge_type"),
        "length_m": specific_data.get("length_m"),
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
