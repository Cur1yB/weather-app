from django.shortcuts import render
from .forms import CityForm
from .api import get_weather, get_coordinates
from django.contrib.auth.decorators import login_required
from .models import SearchHistory


@login_required
def history_view(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-search_date')
    return render(request, 'history.html', {'history': history})


def index(request):
    return render(request, "index.html")


def weather_show(request):
    weather = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city']
            city = get_coordinates(city_name)
            print(f'{city=}, {city_name=}')
            if city:
                weather = get_weather(city)
                SearchHistory.objects.create(user=request.user, city=city_name)
                return render(request, 'weather.html', {"form": form, "weather":weather, 'city_name':city_name})
            else:
                form.add_error('city', 'Unable to find coordinates for this city.')
    if request.method == 'GET':
        form = CityForm()
    return render(request, 'weather.html', {"form": form, 'weather':weather})
