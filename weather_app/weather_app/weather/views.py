from django.shortcuts import render
from .forms import CityForm
from .api import get_weather, get_coordinates
from django.contrib.auth.decorators import login_required
from .models import SearchHistory, CitySearchCount
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from django.db import transaction
from .serializers import CitySearchCountSerializer


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
                search_counter(city=city_name)
                return render(request, 'weather.html', {"form": form, "weather":weather, 'city_name':city_name})
            else:
                form.add_error('city', 'Unable to find coordinates for this city.')
    if request.method == 'GET':
        form = CityForm()
    return render(request, 'weather.html', {"form": form, 'weather':weather})


class CitySearchCountAPI(APIView):
    def get(self, request):
        cities = CitySearchCount.objects.all()
        serializer = CitySearchCountSerializer(cities, many=True)
        return Response(serializer.data)
    

def search_counter(city):
    # Попытка обновить существующую запись
    try:
        with transaction.atomic():
            city_count = CitySearchCount.objects.select_for_update().get(city=city)
            city_count.search_count = F('search_count') + 1
            city_count.save()
    except CitySearchCount.DoesNotExist:
        # Создание новой записи, если запись не существует
        CitySearchCount.objects.create(city=city, search_count=1)
