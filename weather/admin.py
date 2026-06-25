from django.contrib import admin
from .models import WeatherData, DailyReport

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'city', 'temperature_avg', 'humidity', 'precipitation', 'weather_condition']
    list_filter = ['city', 'weather_condition', 'date']
    search_fields = ['city', 'weather_condition']
    date_hierarchy = 'date'

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'report_date', 'status', 'sent_at']
    list_filter = ['status', 'report_date']
