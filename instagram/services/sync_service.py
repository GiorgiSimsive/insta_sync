from django.db import transaction
from django.utils.dateparse import parse_datetime

from instagram.models import Post
from instagram.services.instagram_client import InstagramClient


@transaction.atomic
def sync_posts(client: InstagramClient, ig_user_id: str) -> int:
    """
    Синхронизирует все посты из Instagram в локальную БД.
    Upsert: если ig_media_id уже существует — обновляем поля.
    Возвращает кол-во обработанных медиа.
    """
    media_items = client.fetch_all_user_media(ig_user_id)

    for item in media_items:
        ig_media_id = item.get("id")
        if not ig_media_id:
            continue

        raw_ts = item.get("timestamp")
        ts = parse_datetime(raw_ts) if isinstance(raw_ts, str) else None

        Post.objects.update_or_create(
            ig_media_id=ig_media_id,
            defaults={
                "caption": item.get("caption") or "",
                "media_type": item.get("media_type") or "",
                "media_url": item.get("media_url") or "",
                "permalink": item.get("permalink") or "",
                "timestamp": ts,
                "username": item.get("username") or "",
            },
        )

    return len(media_items)
