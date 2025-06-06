from rest_framework import serializers
from .models import Post, Comment, Like, Bookmark


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    bookmark_count = serializers.IntegerField(source="bookmarks.count", read_only=True)
    liked = serializers.SerializerMethodField()
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )  # 카테고리 한글 이름

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "category",
            "category_display",  # 필드 추가
            "title",
            "content",
            "created_at",
            "comments",
            "like_count",
            "bookmark_count",
            "liked",
            "views",  # views 필드 추가
        ]

    def get_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
