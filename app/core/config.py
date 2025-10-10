from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "FastAPI App"
    sqlite_url: str = "sqlite:///./app.db"


settings = Settings()
