from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.bridge import Bridge
from app.schemas.bridge import BridgeCreate, BridgeRead
from app.services.mappers import bridge_to_read

router = APIRouter(prefix="/bridges", tags=["bridges"])


@router.get("/", response_model=list[BridgeRead])
def list_bridges(db: Session = Depends(get_db)):
    models = db.execute(select(Bridge)).scalars().all()
    return [bridge_to_read(m) for m in models]


@router.post("/", response_model=BridgeRead, summary="Создать новый мост")
def create_bridge(bridge: BridgeCreate, db: Session = Depends(get_db)):
    db_bridge = Bridge(
        name=bridge.name,
        owner=bridge.owner,
        year_commissioned=bridge.year_commissioned,
        bridge_type=bridge.bridge_type,
        length_m=bridge.length_m,
        centroid_lat=bridge.centroid.lat,
        centroid_lon=bridge.centroid.lon,
    )

    db.add(db_bridge)
    db.commit()
    db.refresh(db_bridge)

    return bridge_to_read(db_bridge)
