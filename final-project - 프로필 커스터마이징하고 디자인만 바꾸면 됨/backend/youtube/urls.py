from django.urls import path
from .views import (
    YouTubeSearchView,
    YouTubeVideoDetailView,
    YouTubeChannelDetailView,
)

urlpatterns = [
    path("search/", YouTubeSearchView.as_view(), name="youtube-search"),
    path("videos/", YouTubeVideoDetailView.as_view(), name="youtube-video-detail"),
    path(
        "channels/", YouTubeChannelDetailView.as_view(), name="youtube-channel-detail"
    ),
]
