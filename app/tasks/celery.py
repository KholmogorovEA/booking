from celery import Celery
from app.config import settings


celery = Celery(
    'task',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=["app.tasks.tasks"],
)
