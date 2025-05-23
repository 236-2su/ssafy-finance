from django.urls import path
from . import views

app_name = "saving"

urlpatterns = [
    path("saving-products/", views.saving_product, name="saving_product"),
    path(
        "saving-products-options/<str:fin_prdt_cd>/",
        views.option_list,
        name="saving_option_list",
    ),
    path(
        "saving-products-detail/<str:fin_prdt_cd>/",
        views.product_detail,
        name="saving_product_detail",
    ),
]
