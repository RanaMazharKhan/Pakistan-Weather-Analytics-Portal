from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create an active admin superuser for testing the admin panel'

    def handle(self, *args, **options):
        username = 'admin_user'
        email = 'admin_user@pakweather.com'
        password = 'AdminPassword123'
        
        user, created = User.objects.get_or_create(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully created superuser: '{username}' with password: '{password}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists. Password updated and privileges verified."))
