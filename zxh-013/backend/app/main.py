from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import markers, votes, heatmap, subscriptions, routes, leaderboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CityRadar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(markers.router)
app.include_router(votes.router)
app.include_router(heatmap.router)
app.include_router(subscriptions.router)
app.include_router(routes.router)
app.include_router(leaderboard.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
