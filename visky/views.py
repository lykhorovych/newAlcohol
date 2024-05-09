from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Alcohol
from .forms import AlcoForm
# Create your views here.


class AlcoholListView(ListView):
    model = Alcohol
    template_name = 'visky/all.html'
    #context_object_name = 'alcohols'

    def get_queryset(self):
        return Alcohol.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        form = AlcoForm()
        return {
            'form': form,
            'alcohols': self.get_queryset()
        }


class DetailAlco(DetailView):
    model = Alcohol
    template_name = "visky/detail.html"
    context_object_name = "alcohol"


class SearchAlcoholView(ListView):
    template_name = 'visky/all.html'
    #context_object_name = 'alcohols'

    def get_queryset(self):
        q = self.request.GET.get('q')
        alcohols = Alcohol.objects.filter(name__contains=q.title()).all()
        return alcohols

    def get_context_data(self, **kwargs):
        return {'alcohols': self.get_queryset(),
                'q': self.request.GET.get('q'),
                'form': AlcoForm(),
                }
