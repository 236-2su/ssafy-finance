from django.urls import path
from .views import StockSearchView

app_name = "main"

urlpatterns = [
    path("stocks/search/", StockSearchView.as_view(), name="stock_search"),
]
