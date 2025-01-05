FROM python:3.12-slim


# Installing poetry
RUN pip install --upgrade pip poetry && pip cache purge
ENV PATH="/root/.local/bin:$PATH" 
ENV PYTHONUNBUFFERED=1 

# Enabling environment and transfering files
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-cache
COPY . ./
