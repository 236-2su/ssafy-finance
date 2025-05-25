# community/urls.py

from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    CommentListCreateView,
    CommentRetrieveDestroyView,
    LikeToggleView,
    BookmarkToggleView,
)

urlpatterns = [
    # 게시글 목록 조회 / 생성
    path("posts/", PostListCreateView.as_view()),
    # 게시글 상세 조회 / 수정 / 삭제
    path("posts/<int:pk>/", PostRetrieveUpdateDestroyView.as_view()),
    # 댓글 목록 조회 / 생성
    path("posts/<int:pk>/comments/", CommentListCreateView.as_view()),
    # 댓글 상세 조회 / 삭제 (nested)
    path(
        "posts/<int:post_pk>/comments/<int:pk>/",
        CommentRetrieveDestroyView.as_view(),
    ),
    # 좋아요 토글
    path("posts/<int:pk>/like/", LikeToggleView.as_view()),
    # 북마크 토글
    path("posts/<int:pk>/bookmark/", BookmarkToggleView.as_view()),
]
