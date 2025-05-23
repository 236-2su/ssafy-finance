# community/views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like, Bookmark
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


# ─ 게시글 목록 조회 / 생성 ───────────────────────────────
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # ?category=free 등 필터링
        category = self.request.query_params.get("category")
        if category in dict(Post.CATEGORY_CHOICES):
            return Post.objects.filter(category=category).order_by("-created_at")
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ─ 게시글 상세 조회 / 수정 / 삭제 ──────────────────────────
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user
        )  # 수정시에도 작성자는 로그인한 유저로 유지됩니다.


# ─ 댓글 목록 조회 / 생성 ─────────────────────────────────
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["pk"]).order_by("created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(author=self.request.user, post=post)


# ─ 댓글 상세 조회 / 삭제 ─────────────────────────────────
class CommentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]


# ─ 좋아요 토글 ────────────────────────────────────────
class LikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        obj, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            obj.delete()
            return Response({"liked": False, "count": post.likes.count()})
        return Response({"liked": True, "count": post.likes.count()})


# ─ 북마크(스크랩) 토글 ──────────────────────────────────
class BookmarkToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        obj, created = Bookmark.objects.get_or_create(post=post, user=request.user)
        if not created:
            obj.delete()
            return Response({"bookmarked": False, "count": post.bookmarks.count()})
        return Response({"bookmarked": True, "count": post.bookmarks.count()})


# 게시글 삭제
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user
        )  # 수정시에도 작성자는 로그인한 유저로 유지됩니다.

    def perform_destroy(self, instance):
        # 삭제 전 추가적인 로직이 필요하다면 작성
        instance.delete()
