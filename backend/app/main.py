from fastapi import FastAPI

app = FastAPI(title="Financial Terminal API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
