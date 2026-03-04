from django.conf import settings
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from instagram.models import Comment, Post
from instagram.pagination import PostCursorPagination
from instagram.serializers import CommentSerializer, PostSerializer
from instagram.services.exceptions import InstagramAPIError, InstagramNotFoundError
from instagram.services.instagram_client import InstagramClient
from instagram.services.sync_service import sync_posts


class SyncView(APIView):
    """
    POST /api/sync/
    Синхронизирует все медиа из Instagram -> в БД.
    """

    def post(self, request, *args, **kwargs):
        if not settings.IG_ACCESS_TOKEN or not settings.IG_USER_ID:
            return Response(
                {"detail": "IG_ACCESS_TOKEN / IG_USER_ID not set"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        client = InstagramClient(
            base_url=settings.IG_GRAPH_BASE_URL,
            access_token=settings.IG_ACCESS_TOKEN,
        )

        try:
            processed = sync_posts(client=client, ig_user_id=settings.IG_USER_ID)
        except InstagramAPIError as e:
            return Response(
                {"detail": "Instagram API error", "error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({"processed": processed}, status=status.HTTP_200_OK)


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination
    queryset = Post.objects.all().order_by("-created_at", "-id")


class CreateCommentView(APIView):
    """
    POST /api/posts/{id}/comment/
    {id} — внутренний PK поста в нашей БД.
    """

    def post(self, request, id: int, *args, **kwargs):
        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "text is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post_obj = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        client = InstagramClient(
            base_url=settings.IG_GRAPH_BASE_URL,
            access_token=settings.IG_ACCESS_TOKEN,
        )

        try:
            ig_resp = client.create_comment(ig_media_id=post_obj.ig_media_id, message=text)
        except InstagramNotFoundError:
            return Response({"detail": "Post not found in Instagram"}, status=status.HTTP_404_NOT_FOUND)
        except InstagramAPIError as e:
            return Response({"detail": "Instagram API error", "error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        comment = Comment.objects.create(
            post=post_obj,
            ig_comment_id=ig_resp.get("id", "") or "",
            text=text,
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
