from django.urls import path
from . import views

app_name = "ai_recommendations"

urlpatterns = [
    path("recommend/", views.get_ai_recommendation, name="get_ai_recommendation"),
]
