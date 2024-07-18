from rest_framework import serializers
from .models import CitySearchCount

class CitySearchCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitySearchCount
        fields = ('city', 'search_count')