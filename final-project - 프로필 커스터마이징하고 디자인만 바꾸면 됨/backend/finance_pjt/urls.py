from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/main/", include("main.urls")),  # 추가
    path("api/accounts/", include("accounts.urls")),
    path("api/community/", include("community.urls")),
    path("api/youtube/", include("youtube.urls")),
    path("api/commodities/", include("commodities.urls")),
    path("saving/", include("saving.urls")),
]
