from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.widgets import router as widgets_router
from app.routers.submissions import router as submissions_router

app = FastAPI(
    title="FlyRank Widget Platform",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(widgets_router)
app.include_router(submissions_router)

@app.get("/")
def root():
    return {
        "message": "FlyRank Widget Platform API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }