from django.core.management.base import BaseCommand

from weather.services import sync_weather_data


class Command(BaseCommand):
    help = 'Fetch weather data from Open-Meteo API for all Pakistani cities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days of weather history to fetch (max 92)',
        )

    def handle(self, *args, **options):
        days = min(options['days'], 92)
        self.stdout.write(f'Fetching {days} days of weather data from Open-Meteo...')

        result = sync_weather_data(days=days)

        if result['errors']:
            for error in result['errors']:
                self.stderr.write(self.style.WARNING(error))

        self.stdout.write(
            self.style.SUCCESS(
                f"Saved {result['saved']} records for {result['cities']} cities "
                f"({result['start_date']} to {result['end_date']})"
            )
        )
