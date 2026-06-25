from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    receive_daily_reports = models.BooleanField(default=True)
    preferred_cities = models.CharField(max_length=500, blank=True, null=True, 
                                         help_text="Comma-separated city names")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_preferred_cities_list(self):
        if self.preferred_cities:
            return [city.strip() for city in self.preferred_cities.split(',') if city.strip()]
        return []
