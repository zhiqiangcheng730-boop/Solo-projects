from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
from errors import AppError, app_error_handler
from routers import (
    user_router, skill_router, transaction_router,
    matching_router, review_router, location_router,
    urgent_router, ranking_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="技能时间银行", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

app.include_router(user_router)
app.include_router(skill_router)
app.include_router(transaction_router)
app.include_router(matching_router)
app.include_router(review_router)
app.include_router(location_router)
app.include_router(urgent_router)
app.include_router(ranking_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
