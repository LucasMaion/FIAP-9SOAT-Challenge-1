FROM python:3.12-rc-slim-buster AS builder

# Install dependencies
# python3-venv is required for poetry
# libpq-dev, python-dev, gcc are required for psycopg2
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv libpq-dev python-dev gcc
ENV PATH="/root/.local/bin:${PATH}"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache 
RUN python3 -m pip install poetry

WORKDIR /app
COPY builder.py app.py pyproject.toml ./
RUN poetry lock --no-update && poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DI

FROM builder AS dev

WORKDIR /app
COPY builder.py app.py pyproject.toml ./
COPY ./migration ./migration
COPY ./src ./src
COPY ./tests ./tests
RUN poetry lock --no-update && poetry install --no-root && rm -rf $POETRY_CACHE_DIR
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

FROM builder AS prd

WORKDIR /app
COPY builder.py app.py pyproject.toml ./
COPY ./migration ./migration
COPY ./src ./src
RUN poetry run python3 builder.py -b
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]