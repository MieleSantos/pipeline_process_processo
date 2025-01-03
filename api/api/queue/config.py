from celery import Celery


celery = Celery(
    "tasks",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)

# Configuração adicional (opcional)
celery.conf.task_routes = {"tasks.*": {"queue": "default"}}
