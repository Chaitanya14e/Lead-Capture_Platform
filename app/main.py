from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.middleware.rate_limit import limiter
from app.routers.auth import router as auth_router
from app.routers.submissions import router as submissions_router
from app.routers.widgets import router as widgets_router


app = FastAPI(
    title="FlyRank Widget Platform",
    version="1.0.0",
)


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
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