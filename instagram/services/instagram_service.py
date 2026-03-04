import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_instagram_media():
    base_url = os.getenv("IG_GRAPH_BASE_URL")
    access_token = os.getenv("IG_ACCESS_TOKEN")
    ig_user_id = os.getenv("IG_USER_ID")

    url = f"{base_url}/{ig_user_id}/media"

    params = {
        "fields": "id,caption,media_type,media_url,permalink,timestamp",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    return response.json()
