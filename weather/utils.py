import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .models import WeatherData


def get_filtered_data(city=None, date_from=None, date_to=None, temp_min=None, temp_max=None, sort_by='-date'):
    queryset = WeatherData.objects.all()
    if city:
        queryset = queryset.filter(city=city)
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if temp_min is not None:
        queryset = queryset.filter(temperature_avg__gte=temp_min)
    if temp_max is not None:
        queryset = queryset.filter(temperature_avg__lte=temp_max)
    if sort_by:
        queryset = queryset.order_by(sort_by)
    return queryset


def calculate_statistics(queryset):
    df = WeatherData.get_dataframe(queryset)
    if df.empty:
        return None
    return {
        'total_records': len(df),
        'date_range': {'start': df['date'].min().strftime('%Y-%m-%d'), 'end': df['date'].max().strftime('%Y-%m-%d')},
        'cities_count': df['city'].nunique(),
        'cities_list': df['city'].unique().tolist(),
        'temperature': {
            'avg_max': round(df['temperature_max'].mean(), 1),
            'avg_min': round(df['temperature_min'].mean(), 1),
            'avg_avg': round(df['temperature_avg'].mean(), 1),
            'overall_max': round(df['temperature_max'].max(), 1),
            'overall_min': round(df['temperature_min'].min(), 1),
        },
        'humidity': {'average': round(df['humidity'].mean(), 1), 'max': round(df['humidity'].max(), 1), 'min': round(df['humidity'].min(), 1)},
        'precipitation': {'total': round(df['precipitation'].sum(), 1), 'average': round(df['precipitation'].mean(), 1), 'max': round(df['precipitation'].max(), 1), 'rainy_days': len(df[df['precipitation'] > 0])},
        'wind_speed': {'average': round(df['wind_speed'].mean(), 1), 'max': round(df['wind_speed'].max(), 1)},
    }


def generate_insights(queryset):
    df = WeatherData.get_dataframe(queryset)
    if df.empty:
        return ["No data available to generate insights."]
    insights = []
    
    if 'temperature_max' in df.columns:
        max_temp_row = df.loc[df['temperature_max'].idxmax()]
        min_temp_row = df.loc[df['temperature_min'].idxmin()]
        insights.append(f"Hottest day: {max_temp_row['date'].strftime('%B %d, %Y')} in {max_temp_row['city']} with {max_temp_row['temperature_max']}C")
        insights.append(f"Coldest day: {min_temp_row['date'].strftime('%B %d, %Y')} in {min_temp_row['city']} with {min_temp_row['temperature_min']}C")
    
    df['month'] = df['date'].dt.month
    monthly_avg = df.groupby('month')['temperature_avg'].mean()
    if not monthly_avg.empty:
        month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        hottest_month = monthly_avg.idxmax()
        coldest_month = monthly_avg.idxmin()
        insights.append(f"Hottest month: {month_names.get(hottest_month, 'Unknown')} ({monthly_avg[hottest_month]:.1f}C)")
        insights.append(f"Coldest month: {month_names.get(coldest_month, 'Unknown')} ({monthly_avg[coldest_month]:.1f}C)")
    
    if 'precipitation' in df.columns:
        total_rain = df['precipitation'].sum()
        rainy_days = len(df[df['precipitation'] > 0])
        insights.append(f"Total precipitation: {total_rain:.1f}mm over {rainy_days} rainy days")
        city_rain = df.groupby('city')['precipitation'].sum()
        if not city_rain.empty:
            rainiest_city = city_rain.idxmax()
            insights.append(f"Rainiest city: {rainiest_city} with {city_rain[rainiest_city]:.1f}mm")
    
    if 'city' in df.columns and df['city'].nunique() > 1:
        city_temps = df.groupby('city')['temperature_avg'].mean()
        insights.append(f"Hottest city: {city_temps.idxmax()} ({city_temps.max():.1f}C)")
        insights.append(f"Coolest city: {city_temps.idxmin()} ({city_temps.min():.1f}C)")
    
    return insights


def get_chart_data(queryset, chart_type='line'):
    df = WeatherData.get_dataframe(queryset)
    if df.empty:
        return None
    
    if chart_type == 'line':
        df_sorted = df.sort_values('date')
        if df['city'].nunique() == 1:
            return {
                'labels': df_sorted['date'].dt.strftime('%Y-%m-%d').tolist(),
                'datasets': [
                    {'label': 'Max Temp (C)', 'data': df_sorted['temperature_max'].tolist(), 'borderColor': 'rgba(255, 99, 132, 1)', 'backgroundColor': 'rgba(255, 99, 132, 0.2)', 'fill': False, 'tension': 0.4},
                    {'label': 'Min Temp (C)', 'data': df_sorted['temperature_min'].tolist(), 'borderColor': 'rgba(54, 162, 235, 1)', 'backgroundColor': 'rgba(54, 162, 235, 0.2)', 'fill': False, 'tension': 0.4},
                    {'label': 'Avg Temp (C)', 'data': df_sorted['temperature_avg'].tolist(), 'borderColor': 'rgba(75, 192, 192, 1)', 'backgroundColor': 'rgba(75, 192, 192, 0.2)', 'fill': False, 'tension': 0.4}
                ]
            }
        else:
            city_data = df.groupby('city')['temperature_avg'].mean().round(1)
            return {'labels': city_data.index.tolist(), 'datasets': [{'label': 'Avg Temp (C)', 'data': city_data.values.tolist(), 'backgroundColor': 'rgba(75, 192, 192, 0.6)', 'borderColor': 'rgba(75, 192, 192, 1)', 'borderWidth': 2}]}
    
    elif chart_type == 'bar':
        city_precip = df.groupby('city')['precipitation'].sum().round(1)
        colors = ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)']
        return {'labels': city_precip.index.tolist(), 'datasets': [{'label': 'Total Precipitation (mm)', 'data': city_precip.values.tolist(), 'backgroundColor': colors[:len(city_precip)], 'borderWidth': 1}]}
    
    elif chart_type == 'pie':
        condition_counts = df['weather_condition'].value_counts()
        colors = ['rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)']
        return {'labels': condition_counts.index.tolist(), 'datasets': [{'data': condition_counts.values.tolist(), 'backgroundColor': colors[:len(condition_counts)], 'borderWidth': 2}]}
    
    elif chart_type == 'histogram':
        temp_bins = [-10, 0, 10, 20, 30, 40, 50]
        temp_labels = ['<0C', '0-10C', '10-20C', '20-30C', '30-40C', '40C+']
        temp_counts = pd.cut(df['temperature_avg'], bins=temp_bins, labels=temp_labels).value_counts().sort_index()
        return {'labels': temp_labels, 'datasets': [{'label': 'Number of Days', 'data': temp_counts.values.tolist(), 'backgroundColor': 'rgba(75, 192, 192, 0.6)'}]}
    
    elif chart_type == 'scatter':
        return {'datasets': [{'label': 'Temp vs Humidity', 'data': [{'x': row['temperature_avg'], 'y': row['humidity']} for _, row in df.iterrows()], 'backgroundColor': 'rgba(54, 162, 235, 0.6)', 'pointRadius': 5}]}
    
    return None

def get_daily_report_data(cities=None):
    """
    Get data for daily email reports.
    """
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    if cities:
        queryset = WeatherData.objects.filter(
            city__in=cities,
            date=yesterday
        )
    else:
        queryset = WeatherData.objects.filter(date=yesterday)
    
    df = WeatherData.get_dataframe(queryset)
    
    if df.empty:
        # If no data for yesterday, get the most recent data
        queryset = WeatherData.objects.filter(
            city__in=cities if cities else WeatherData.objects.values_list('city', flat=True).distinct()
        ).order_by('-date')[:100]
        df = WeatherData.get_dataframe(queryset)
    
    return df