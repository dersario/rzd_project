import uvicorn

from app.main import setup_app


def main() -> None:
    app = setup_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )


if __name__ == "__main__":
    main()
