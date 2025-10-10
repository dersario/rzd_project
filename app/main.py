from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import engine
from app.models import Base
from app.routers.embankments import router as embankments_router
from app.routers.items import router as items_router
from app.routers.pipelines import router as pipelines_router
from app.routers.powerlines import router as powerlines_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # seed after tables are created
    try:
        from app.db.session import SessionLocal
        from app.services.seed import seed_all

        db = SessionLocal()
        try:
            seed_all(db)
        finally:
            db.close()
    except Exception:
        pass
    yield


app = FastAPI(title="FastAPI App", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(items_router)
app.include_router(powerlines_router)
app.include_router(pipelines_router)
app.include_router(embankments_router)
