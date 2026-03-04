import requests

from instagram.services.exceptions import InstagramAPIError, InstagramNotFoundError


class InstagramClient:
    """
    Клиент для Instagram Graph API.
    Вся интеграция с requests живёт тут, а не во views.
    """

    def __init__(self, base_url: str, access_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token

    def _get(self, path: str, params: dict) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = {**params, "access_token": self.access_token}

        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        if resp.status_code >= 400 or "error" in data:
            raise InstagramAPIError(str(data))

        return data

    def _post(self, path: str, params: dict) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = {**params, "access_token": self.access_token}

        resp = requests.post(url, params=params, timeout=15)
        data = resp.json()

        if resp.status_code >= 400 or "error" in data:
            error = data.get("error", {})
            msg = str(data).lower()
            if resp.status_code == 404 or "not found" in msg:
                raise InstagramNotFoundError(str(data))
            raise InstagramAPIError(str(data))

        return data

    def fetch_all_user_media(self, ig_user_id: str) -> list[dict]:
        """
        Забирает ВСЕ медиа пользователя, проходя по paging.next пока он есть.
        """
        fields = "id,caption,media_type,media_url,permalink,timestamp,username"

        payload = self._get(
            path=f"{ig_user_id}/media",
            params={"fields": fields, "limit": 25},
        )

        items: list[dict] = []

        while True:
            items.extend(payload.get("data", []))

            next_url = payload.get("paging", {}).get("next")
            if not next_url:
                break

            resp = requests.get(next_url, timeout=15)
            payload = resp.json()
            if resp.status_code >= 400 or "error" in payload:
                raise InstagramAPIError(str(payload))

        return items

    def create_comment(self, ig_media_id: str, message: str) -> dict:
        """
        Создаёт комментарий для медиа.
        POST /{ig_media_id}/comments?message=...
        """
        return self._post(path=f"{ig_media_id}/comments", params={"message": message})
