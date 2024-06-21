from celery import Celery
from os import getenv

celery_app = Celery(
    "tasks", broker=getenv("CELERY_BROKER_URL"), backend=getenv("CELERY_RESULT_BACKEND")
)

celery_app.conf.update(
    result_expires=3600,
    task_track_started=True,
)

if __name__ == "__main__":
    celery_app.start()
