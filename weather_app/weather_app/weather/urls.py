from django.urls import path
from .views import index, weather_show, history_view, CitySearchCountAPI

app_name = 'weather'

urlpatterns = [
    path("", index, name='index'),
    path("get_weather/", weather_show, name='weather_show'),
    path('history/', history_view, name='history_view'),
    path('api/search-count/', CitySearchCountAPI.as_view(), name='city-search-count-api')
]