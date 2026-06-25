import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import WeatherData, DailyReport
from .utils import calculate_statistics, generate_insights
from .services import ensure_weather_data

logger = logging.getLogger(__name__)


def send_daily_reports():
    from accounts.models import UserProfile
    from django.contrib.auth.models import User

    ensure_weather_data()

    for user in User.objects.filter(is_active=True).exclude(email=''):
        UserProfile.objects.get_or_create(user=user)

    today = timezone.localdate()
    profiles = UserProfile.objects.filter(
        user__is_active=True,
        user__email__gt='',
        receive_daily_reports=True,
    ).select_related('user')

    sent_count, failed_count, skipped_count = 0, 0, 0
    for profile in profiles:
        user = profile.user
        if DailyReport.objects.filter(user=user, report_date=today, status='sent').exists():
            skipped_count += 1
            continue

        try:
            success = send_daily_report_to_user(user, today)
            DailyReport.objects.update_or_create(
                user=user,
                report_date=today,
                defaults={
                    'cities_included': ', '.join(profile.get_preferred_cities_list()) or 'All',
                    'status': 'sent' if success else 'failed',
                    'error_message': '' if success else 'No weather data available for report.',
                },
            )
            if success:
                sent_count += 1
            else:
                failed_count += 1
        except Exception as exc:
            logger.exception('Error sending daily report to %s', user.email)
            DailyReport.objects.update_or_create(
                user=user,
                report_date=today,
                defaults={
                    'cities_included': ', '.join(profile.get_preferred_cities_list()) or 'All',
                    'status': 'failed',
                    'error_message': str(exc),
                },
            )
            failed_count += 1

    return sent_count, failed_count, skipped_count


def _get_report_queryset(user, report_date):
    from accounts.models import UserProfile

    try:
        profile = UserProfile.objects.get(user=user)
        cities = profile.get_preferred_cities_list()
    except UserProfile.DoesNotExist:
        cities = []

    yesterday = report_date - timedelta(days=1)
    queryset = WeatherData.objects.filter(date=yesterday)
    if cities:
        queryset = queryset.filter(city__in=cities)

    if queryset.exists():
        return queryset, yesterday

    fallback = WeatherData.objects.all()
    if cities:
        fallback = fallback.filter(city__in=cities)
    latest_date = fallback.order_by('-date').values_list('date', flat=True).first()
    if not latest_date:
        return WeatherData.objects.none(), yesterday

    return fallback.filter(date=latest_date), latest_date


def send_daily_report_to_user(user, report_date):
    queryset, data_date = _get_report_queryset(user, report_date)
    if not queryset.exists():
        return False

    stats = calculate_statistics(queryset)
    insights = generate_insights(queryset)
    city_summary = [
        {
            'city': record.city,
            'temp_max': record.temperature_max,
            'temp_min': record.temperature_min,
            'temp_avg': record.temperature_avg,
            'humidity': record.humidity,
            'precipitation': record.precipitation,
            'condition': record.weather_condition,
        }
        for record in queryset
    ]

    subject = f'Daily Weather Report - {data_date.strftime("%B %d, %Y")}'
    html_message = render_to_string('weather/email_report.html', {
        'user': user,
        'report_date': data_date,
        'stats': stats,
        'insights': insights,
        'city_summary': city_summary,
    })

    send_mail(
        subject,
        f'Your daily weather report for {data_date.strftime("%B %d, %Y")} is ready.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )
    return True
