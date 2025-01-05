from queue.config import celery


@celery.task
def process_pdf(file_content) -> int:
    # Exemplo de tarefa que soma dois números
    return sum(file_content)
