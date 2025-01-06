import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

if not os.getenv('CELERY_BROKER_URL'):
    raise ValueError('CELERY_BROKER_URL not found in .env file')
if not os.getenv('CELERY_RESULT_BACKEND'):
    raise ValueError('CELERY_RESULT_BACKEND not found in .env file')

app = Celery(
    'pipeline_process_processo',
    broker=os.getenv('CELERY_BROKER_URL'),
)

app.conf.update(
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
