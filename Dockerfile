FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# системные зависимости для psycopg/сборок
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry

# зависимости
COPY pyproject.toml poetry.lock* README.md /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# код проекта
COPY . /app/

# запуск: миграции + сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
