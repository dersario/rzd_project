from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.models import Base
from app.routers.accidents import router as accident_router
from app.routers.bridges import router as bridges_router
from app.routers.embankments import router as embankments_router
from app.routers.pipelines import router as pipelines_router
from app.routers.powerlines import router as powerlines_router
from app.routers.search import router as search_router
from app.routers.users import users_routers
from app.settings import Settings


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


def setup_app():
    app = FastAPI(title="RZD Project", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    settings = Settings()
    app.state.token_secret = settings.token_secret

    app.include_router(users_routers)
    app.include_router(powerlines_router)
    app.include_router(pipelines_router)
    app.include_router(embankments_router)
    app.include_router(bridges_router)
    app.include_router(accident_router)
    app.include_router(search_router)
    return app
