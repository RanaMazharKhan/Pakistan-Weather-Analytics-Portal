from django.core.management.base import BaseCommand

from weather.services import ensure_weather_data
from weather.tasks import send_daily_reports


class Command(BaseCommand):
    help = 'Send daily weather report emails to all active subscribed users'

    def handle(self, *args, **options):
        self.stdout.write('Syncing latest weather data...')
        ensure_weather_data()

        self.stdout.write('Sending daily weather reports...')
        sent, failed, skipped = send_daily_reports()

        self.stdout.write(
            self.style.SUCCESS(
                f'Daily reports complete: {sent} sent, {failed} failed, {skipped} skipped (already sent today).'
            )
        )
