from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import NewsArticle
from .serializers import NewsArticleSerializer, NewsArticleListSerializer
from .crawler import NaverFinanceCrawler

class NewsArticleListView(generics.ListAPIView):
    """뉴스 기사 목록 조회"""
    serializer_class = NewsArticleListSerializer
    
    def get_queryset(self):
        queryset = NewsArticle.objects.all()
        
        # 카테고리 필터링
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # 최근 7일 뉴스만 조회
        week_ago = timezone.now() - timedelta(days=7)
        queryset = queryset.filter(published_date__gte=week_ago)
        
        return queryset[:20]  # 최대 20개

class NewsArticleDetailView(generics.RetrieveAPIView):
    """뉴스 기사 상세 조회"""
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

@api_view(['POST'])
def crawl_news(request):
    """뉴스 크롤링 실행"""
    try:
        crawler = NaverFinanceCrawler()
        saved_count = crawler.crawl_and_save(max_pages=2)
        
        return Response({
            'success': True,
            'message': f'{saved_count}개의 새로운 뉴스를 저장했습니다.',
            'saved_count': saved_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'뉴스 크롤링 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def latest_news(request):
    """최신 뉴스 5개 조회 (메인페이지용)"""
    try:
        latest_articles = NewsArticle.objects.all()[:5]
        serializer = NewsArticleListSerializer(latest_articles, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'뉴스 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
