from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.widgets import router as widgets_router
from app.routers.submissions import router as submissions_router


app = FastAPI(
    title="FlyRank Widget Platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
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