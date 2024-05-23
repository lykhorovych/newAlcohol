import io
import urllib, base64
from typing import Any
import urllib.parse
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Alcohol
from .forms import AlcoForm
from django.core.paginator import Paginator
import plotly.graph_objects as go 
# Create your views here.


def index(request):
    form = AlcoForm()
    q = request.GET.get('q')
    data = Alcohol.objects.filter(name__icontains=q) if q else Alcohol.objects.all()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('HX-Request') == 'true':

        return render(request, 'visky/alcohol_list.html', {'page_obj': page_obj, 'q': q})

    return render(request, 'visky/index.html', {'page_obj': page_obj, 
                                                'form': form})


class DetailAlco(DetailView):
    model = Alcohol
    template_name = "visky/detail.html"
    context_object_name = "alcohol"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        alcohol = Alcohol.objects.get(pk=pk)
    
        dates = [k for d in alcohol.prices for k in d]
        prices = [k for d in alcohol.prices for k in d.values()]

        fig = go.Figure([go.Scatter(x=dates, y=prices)])
        fig = fig.to_image(format='png')

        context['alcohol'] = alcohol
        context['fig'] = base64.b64encode(fig).decode()

        return context
    