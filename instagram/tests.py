from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.test import APIClient

from instagram.models import Comment, Post


class CreateCommentTests(TestCase):
    def setUp(self):
        self.api = APIClient()

    @patch("instagram.services.instagram_client.requests.post")
    def test_create_comment_success(self, mock_post):
        post = Post.objects.create(ig_media_id="1789_test", caption="hi")

        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"id": "1234567890"},
        )

        resp = self.api.post(
            f"/api/posts/{post.id}/comment/",
            data={"text": "hello"},
            format="json",
        )

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Comment.objects.filter(post=post, text="hello").exists())
        self.assertEqual(resp.data["ig_comment_id"], "1234567890")
        self.assertEqual(resp.data["text"], "hello")

    def test_create_comment_post_not_found_in_db(self):
        resp = self.api.post(
            "/api/posts/999999/comment/",
            data={"text": "hello"},
            format="json",
        )
        self.assertEqual(resp.status_code, 404)

    @patch("instagram.services.instagram_client.requests.post")
    def test_create_comment_post_missing_in_instagram(self, mock_post):
        post = Post.objects.create(ig_media_id="1789_missing", caption="hi")

        mock_post.return_value = Mock(
            status_code=404,
            json=lambda: {"error": {"message": "not found"}},
        )

        resp = self.api.post(
            f"/api/posts/{post.id}/comment/",
            data={"text": "hello"},
            format="json",
        )

        self.assertEqual(resp.status_code, 404)
        self.assertFalse(Comment.objects.filter(post=post).exists())
