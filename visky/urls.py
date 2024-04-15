from django.urls import path
from .views import SearchAlcoholView, AlcoholListView

urlpatterns = [path('', AlcoholListView.as_view(), name='all'),
               path('search/', SearchAlcoholView.as_view(), name='search')]