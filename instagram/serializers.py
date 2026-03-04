from rest_framework import serializers

from instagram.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "ig_media_id",
            "caption",
            "media_type",
            "media_url",
            "permalink",
            "timestamp",
            "username",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "ig_comment_id", "text", "created_at")
        read_only_fields = ("id", "post", "ig_comment_id", "created_at")
