from django.db import models


class Post(models.Model):
    """
    Пост, сохранённый локально, синхронизируется из Instagram Graph API.
    """

    ig_media_id = models.CharField(max_length=64, unique=True)
    caption = models.TextField(blank=True, default="")
    media_type = models.CharField(max_length=32, blank=True, default="")
    media_url = models.TextField(blank=True, default="")
    permalink = models.TextField(blank=True, default="")
    timestamp = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=128, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Post(id={self.id}, ig_media_id={self.ig_media_id})"


class Comment(models.Model):
    """
    Комментарий, созданный через наш API и отправленный в Instagram.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    ig_comment_id = models.CharField(max_length=64, blank=True, default="")
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment(id={self.id}, post_id={self.post_id})"
