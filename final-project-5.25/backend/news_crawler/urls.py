from django.urls import path
from . import views

app_name = 'news_crawler'

urlpatterns = [
    path('', views.NewsArticleListView.as_view(), name='news-list'),
    path('<int:pk>/', views.NewsArticleDetailView.as_view(), name='news-detail'),
    path('crawl/', views.crawl_news, name='crawl-news'),
    path('latest/', views.latest_news, name='latest-news'),
]
