from django.urls import path

from instagram.views import CreateCommentView, PostDetailAPIView, PostListView, SyncView

urlpatterns = [
    path("sync/", SyncView.as_view(), name="sync"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/<int:id>/comment/", CreateCommentView.as_view(), name="post-comment"),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
]
