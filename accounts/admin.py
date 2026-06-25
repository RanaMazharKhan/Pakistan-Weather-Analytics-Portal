from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'receive_daily_reports', 'created_at']
    list_filter = ['receive_daily_reports', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
