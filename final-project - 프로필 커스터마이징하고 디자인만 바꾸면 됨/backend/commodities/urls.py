from django.urls import path
from .views import price_data

urlpatterns = [
    path("prices/", price_data, name="commodities-price-data"),
]
