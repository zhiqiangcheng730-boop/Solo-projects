from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import UPLOAD_DIR
from .database import init_db
from .routers import recordings, dialects, understanding, vocabulary, game, statistics


def create_app() -> FastAPI:
    app = FastAPI(title="方言声音档案馆", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

    app.include_router(recordings.router)
    app.include_router(dialects.router)
    app.include_router(understanding.router)
    app.include_router(vocabulary.router)
    app.include_router(game.router)
    app.include_router(statistics.router)

    @app.on_event("startup")
    def startup():
        init_db()

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
