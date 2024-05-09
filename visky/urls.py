from django.urls import path

from .views import SearchAlcoholView, AlcoholListView, DetailAlco


urlpatterns = [
    path('', AlcoholListView.as_view(), name='all'),
    path('<int:pk>', DetailAlco.as_view(), name="detail"),
    path('search/', SearchAlcoholView.as_view(), name='search')
]
