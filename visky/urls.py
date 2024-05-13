from django.urls import path

from .views import DetailAlco, index


urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>', DetailAlco.as_view(), name="detail"),
]
