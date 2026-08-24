from fastapi import FastAPI

app = FastAPI(title="Financial Terminal API")

from app.api.router import api_router
app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
