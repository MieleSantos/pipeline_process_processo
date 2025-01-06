import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

from config_celery import app
from utils import create_file

load_dotenv()

url_base = os.getenv('URL_BASE')

if not url_base:
    raise ValueError('URL_BASE not found in .env file')


@app.task
def task_process_files(file: bytes):
    """
     task para processar os arquivos pdf, enviando para api
    Args:
        file (bytes): arquivo pdf em bytes

    Returns:
        json: json com dados da task
    """
    files = {'file_pdf': file}
    url = url_base + 'file'
    response = requests.post(url, files=files)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def data_task_status(task_id):
    """
    Busca os dados da task
    Args:
        task_id (_type_): ID da task
    Raises:
        ValueError: Erro ao buscar data da task
    Returns:
        json: Dado da task com status e dad
    """
    url = url_base + f'tasks/status/{task_id}'
    response = requests.get(url)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def verify_task(task_id):
    """
    Verifica o status da task, fazendo algumas chamadas para api e retorna o
    arquivo caso a task tenha sido concluída com SUCESSO
    Args:
        task_id (_type_): ID da task

    Returns:
        Dataframe: Dataframe com os dados do arquivo
    """
    status = 'PENDING'
    list_status = ['SUCCESS', 'FAILURE']
    try:
        while status not in list_status:
            time.sleep(5)
            status_response = data_task_status(task_id)
            status = status_response.get('status')

            if status == 'SUCCESS':
                csv_link = status_response.get('csv_link')
                return create_file(csv_link)

            elif status == 'FAILURE':
                st.error('Task failed!')
                break
            elif status == 'PENDING':
                st.write('Still processing...')
    except Exception as e:
        st.error(f'Error fetching task status: {e}')
        raise
