from rest_framework import serializers
from .models import NewsArticle

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'content', 'summary', 'url', 'published_date', 'created_at', 'category', 'source', 'image_url']
        read_only_fields = ['id', 'created_at']

class NewsArticleListSerializer(serializers.ModelSerializer):
    """뉴스 목록용 간단한 serializer"""
    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'summary', 'url', 'published_date', 'category', 'source', 'image_url']
