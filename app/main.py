from fastapi import FastAPI

app = FastAPI(
    title="FlyRank Widget Platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "FlyRank Widget Platform API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }