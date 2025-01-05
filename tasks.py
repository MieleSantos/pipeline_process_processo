import time


import requests
import streamlit as st

from config_celery import app
from utils import create_file, url_base


@app.task
def task_process_files(file: bytes):
    files = {"file_pdf": file}
    url = url_base + "file"
    response = requests.post(url, files=files)

    return response.json()


def status_task(task_id):
    url = url_base + f"tasks/status/{task_id}"
    response = requests.get(url)
    return response.json()


def verify_task(task_id):
    status = "PENDING"

    while status not in ["SUCCESS"]:
        time.sleep(5)
        status_response = status_task(task_id)
        status = status_response.get("status")

        if status == "SUCCESS":
            csv_link = status_response.get("csv_link")
            return create_file(csv_link)

        elif status == "FAILURE":
            st.error("Tarefa falhou!")
            break
        elif status == "PENDING":
            st.write("Ainda processando...")
