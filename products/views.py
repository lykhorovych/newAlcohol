from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .models import Product
from django.views.generic import ListView

# Create your views here.


class EconomyListView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 10

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        if self.request.headers.get('HX-Request') == 'true':
            self.template_name = "products/product_list.html"
        return super().render_to_response(context, **response_kwargs)
