# Insta Sync (Django + DRF)

Сервис синхронизирует медиа из Instagram Graph API в локальную БД и позволяет создавать комментарии через API.

## Стек
- Python 3.10+ (в проекте: Python 3.12)
- Django, Django REST Framework
- PostgreSQL
- Docker, Docker Compose
- Poetry

## Переменные окружения (.env)

Создайте файл `.env` в корне проекта:

```env
DJANGO_SECRET_KEY="your-secret-key"
DJANGO_DEBUG=1

POSTGRES_DB=insta_sync
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

IG_ACCESS_TOKEN=PUT_YOUR_TOKEN_HERE
IG_USER_ID=PUT_YOUR_IG_USER_ID_HERE
IG_GRAPH_BASE_URL=https://graph.facebook.com/v19.0

## Environment variables

Create `.env` file based on `.env.template`

```bash
cp .env.template .env