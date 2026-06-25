from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import pandas as pd


class WeatherData(models.Model):
    CITY_CHOICES = [
        ('Lahore', 'Lahore'),
        ('Karachi', 'Karachi'),
        ('Islamabad', 'Islamabad'),
        ('Rawalpindi', 'Rawalpindi'),
        ('Faisalabad', 'Faisalabad'),
        ('Multan', 'Multan'),
        ('Peshawar', 'Peshawar'),
        ('Quetta', 'Quetta'),
        ('Sialkot', 'Sialkot'),
        ('Gujranwala', 'Gujranwala'),
        ('Hyderabad', 'Hyderabad'),
        ('Bahawalpur', 'Bahawalpur'),
    ]
    
    date = models.DateField(help_text="Date of the weather record")
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    temperature_max = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(60)])
    temperature_min = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(60)])
    temperature_avg = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(60)])
    humidity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    precipitation = models.FloatField(validators=[MinValueValidator(0)])
    wind_speed = models.FloatField(validators=[MinValueValidator(0)])
    wind_direction = models.CharField(max_length=20)
    pressure = models.FloatField(validators=[MinValueValidator(800), MaxValueValidator(1200)])
    visibility = models.FloatField(validators=[MinValueValidator(0)])
    weather_condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'city']
        verbose_name_plural = "Weather Data"
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['city']),
            models.Index(fields=['date', 'city']),
        ]

    def __str__(self):
        return f"{self.city} - {self.date} ({self.temperature_avg}C)"

    @classmethod
    def get_dataframe(cls, queryset=None):
        if queryset is None:
            queryset = cls.objects.all()
        data = list(queryset.values('id', 'date', 'city', 'temperature_max', 'temperature_min',
            'temperature_avg', 'humidity', 'precipitation', 'wind_speed',
            'wind_direction', 'pressure', 'visibility', 'weather_condition'))
        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        return pd.DataFrame()

    @classmethod
    def import_from_dataframe(cls, df):
        count = 0
        for _, row in df.iterrows():
            cls.objects.update_or_create(
                date=row['date'], city=row['city'],
                defaults={
                    'temperature_max': row.get('temperature_max', 0),
                    'temperature_min': row.get('temperature_min', 0),
                    'temperature_avg': row.get('temperature_avg', 0),
                    'humidity': row.get('humidity', 0),
                    'precipitation': row.get('precipitation', 0),
                    'wind_speed': row.get('wind_speed', 0),
                    'wind_direction': row.get('wind_direction', 'N'),
                    'pressure': row.get('pressure', 1013),
                    'visibility': row.get('visibility', 10),
                    'weather_condition': row.get('weather_condition', 'Clear'),
                }
            )
            count += 1
        return count


class DailyReport(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='daily_reports')
    report_date = models.DateField()
    sent_at = models.DateTimeField(auto_now_add=True)
    cities_included = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending')
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['user', 'report_date']
        ordering = ['-sent_at']

    def __str__(self):
        return f"Report for {self.user.username} - {self.report_date}"
