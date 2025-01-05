from celery import Celery

app = Celery(
    "pipeline_process_processo",
    broker="amqp://guest:guest@rabbitmq:5672//",
)

app.conf.update(
    result_backend="redis://redis:6379/0",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
