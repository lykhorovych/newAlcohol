from django.shortcuts import render
from .models import Product
from django.views.generic import ListView
# Create your views here.


class EconomyListView(ListView):
    model = Product
    template_name = "products/all_products.html"
    context_object_name = "products"
