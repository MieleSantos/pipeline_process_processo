from celery import shared_task


@shared_task(queue="process_data_api")
def process_data_api(file_content) -> int:
    # Exemplo de tarefa que soma dois números
    return sum(file_content)
