from django.db import models

class SearchHistory(models.Model):
    city = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class CitySearchCount(models.Model):
    city = models.CharField(max_length=100, unique=True)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.city} - {self.search_count}"