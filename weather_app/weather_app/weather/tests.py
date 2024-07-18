from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SearchHistory, CitySearchCount
from .forms import CityForm
from .views import search_counter


class WeatherViewsTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_index_view(self):
        response = self.client.get(reverse('weather:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_weather_show_get(self):
        response = self.client.get(reverse('weather:weather_show'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertIsInstance(response.context['form'], CityForm)

    def test_weather_show_post_valid_city(self):
        response = self.client.post(reverse('weather:weather_show'), {'city': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertIn('weather', response.context)
        self.assertIn('city_name', response.context)
        self.assertEqual(response.context['city_name'], 'New York')
        self.assertTrue(SearchHistory.objects.filter(user=self.user, city='New York').exists())

    def test_weather_show_post_invalid_city(self):
        response = self.client.post(reverse('weather:weather_show'), {'city': 'InvalidCityName'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather.html')
        self.assertFalse(SearchHistory.objects.filter(user=self.user, city='InvalidCityName').exists())
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('city', form.errors)

    def test_history_view(self):
        SearchHistory.objects.create(user=self.user, city='New York')
        response = self.client.get(reverse('weather:history_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')
        self.assertIn('history', response.context)
        self.assertEqual(len(response.context['history']), 1)
        self.assertEqual(response.context['history'][0].city, 'New York')


class CitySearchCountTests(TestCase):

    def test_increment_existing_city(self):
        CitySearchCount.objects.create(city="New York", search_count=1)
        search_counter("New York")
        city_count = CitySearchCount.objects.get(city="New York")
        self.assertEqual(city_count.search_count, 2)

    def test_increment_new_city(self):
        search_counter("Krasnoyarsk")
        city_count = CitySearchCount.objects.get(city="Krasnoyarsk")
        self.assertEqual(city_count.search_count, 1)