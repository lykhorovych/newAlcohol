from django.urls import path
from .views import EconomyListView

urlpatterns = [
    path("", EconomyListView.as_view(), name="product_list")
]
