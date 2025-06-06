from django.urls import path
from .views import (
    SignUpView,
    LogInView,
    LogOutView,
    ProfileView,
    ProfileDetailView,
    SurveyView,
    RecommendationView,
    UserActivityView,
    UserStocksView,
    UserYoutubeView,
    CSRFTokenView,
    CurrentUserView,
    UserScrappedPostsView,  # UserScrappedPostsView 추가
)

urlpatterns = [
    path("csrf-token/", CSRFTokenView.as_view()),
    path("signup/", SignUpView.as_view()),
    path("login/", LogInView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("current-user/", CurrentUserView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/<str:username>/", ProfileDetailView.as_view()),
    path("survey/", SurveyView.as_view()),
    path("recommendations/", RecommendationView.as_view()),
    path("activities/", UserActivityView.as_view()),
    path("stocks/", UserStocksView.as_view()),
    path("youtube/", UserYoutubeView.as_view()),
    path(
        "scrapped-posts/", UserScrappedPostsView.as_view(), name="user_scrapped_posts"
    ),
]
