import requests
from dotenv import load_dotenv
import os

HEADER = {"Content-Type": "multipart/form-data"}


def get_url():
    load_dotenv()
    if not os.getenv("URL"):
        raise ValueError("URL not found")

    return os.getenv("URL")


def send_file(file):
    url_base = get_url()
    url = url_base + "/process/file"
    files = {"file_pdf": file}
    r = requests.post(url, files=files)
    print(r.text)
    return r
