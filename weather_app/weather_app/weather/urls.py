from django.urls import path
from .views import index, weather_show, history_view

app_name = 'weather'

urlpatterns = [
    path("", index, name='index'),
    path("get_weather/", weather_show, name='weather_show'),
    path('history/', history_view, name='history_view')
]