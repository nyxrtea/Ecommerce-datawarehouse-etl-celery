# celery_app.py
from celery import Celery

app = Celery(
    'tasks',
    broker='amqp://guest:guest@localhost:5672//',
    backend='rpc://'
)

app.config_from_object('celeryconfig')

import tasks  # Pastikan tasks.py ada dan berisi task yang ingin didaftarkan
