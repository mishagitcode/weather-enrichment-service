import os

from celery import Celery

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)

celery_app = Celery(
    "weather_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "app.tasks"
    ]
)

celery_app.conf.task_routes = {
    "app.tasks.update_weather_for_city": {
        "queue": "weather"
    }
}
