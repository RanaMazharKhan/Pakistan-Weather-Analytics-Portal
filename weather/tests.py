from django.test import TestCase
from .models import WeatherData
from datetime import date

class WeatherDataModelTest(TestCase):
    def setUp(self):
        WeatherData.objects.create(
            date=date(2024, 1, 15), city='Lahore', temperature_max=25.0, temperature_min=10.0,
            temperature_avg=17.5, humidity=60.0, precipitation=0.0, wind_speed=15.0,
            wind_direction='NE', pressure=1013.25, visibility=10.0, weather_condition='Clear'
        )
    
    def test_creation(self):
        self.assertEqual(WeatherData.objects.count(), 1)
