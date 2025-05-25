from django.urls import path
from .views import SignUpView, LogInView, LogOutView, ProfileView, ProfileDetailView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LogInView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/<str:username>/", ProfileDetailView.as_view()),
]
