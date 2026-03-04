class InstagramAPIError(Exception):
    """Ошибка при обращении к Instagram Graph API."""


class InstagramNotFoundError(InstagramAPIError):
    """Объект не найден в Instagram (например, медиа удалено)."""
