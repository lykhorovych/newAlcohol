from django.shortcuts import render
from django.views.generic import ListView
from .models import Alcohol
# Create your views here.


class AlcoholListView(ListView):
    model = Alcohol
    template_name = 'visky/all.html'
    context_object_name = 'alcohols'


class SearchAlcoholView(ListView):
    template_name = 'visky/all.html'
    model = Alcohol
    context_object_name = 'alcohols'

    def get_queryset(self):
        q = self.request.GET.get('q')
        alcohols = Alcohol.objects.filter(name__contains=q.title()).all()
        return alcohols


    def get_context_data(self, **kwargs):
        return {'alcohols': self.get_queryset(),
                'q': self.request.GET.get('q'),
                }

