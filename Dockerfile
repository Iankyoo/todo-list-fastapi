FROM python:3.13-slim 

ENV POETRY_VIRTUALENVS_CREATE=false 

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd 
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev --no-root

COPY . .

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000"]