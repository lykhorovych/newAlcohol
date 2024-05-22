from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Alcohol
from .forms import AlcoForm
from django.core.paginator import Paginator
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

