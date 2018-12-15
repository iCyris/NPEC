from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from weather_app import caster

def index(request):
    qu = request.GET.get('q', '')
    if (qu):
        weather_app = caster.WeatherCaster()
        results = weather_app.main(cityName=qu)
    else:
        results = []
    context = {
            'results': results
        }
    
    return render(request, 'weather/index.html', context=context)
