from celery import Celery
import os

redis_url = os.environ.get("APP_REDIS_URL", "redis://redis:6379/0")
celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url
)

@celery_app.task
def dummy_task():
    return "ok"
