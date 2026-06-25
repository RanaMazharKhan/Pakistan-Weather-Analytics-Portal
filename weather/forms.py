from django import forms
from django.core.exceptions import ValidationError
from .models import WeatherData
import pandas as pd


class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = ['date', 'city', 'temperature_max', 'temperature_min', 'temperature_avg',
                  'humidity', 'precipitation', 'wind_speed', 'wind_direction', 'pressure', 'visibility', 'weather_condition']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'temperature_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'temperature_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'temperature_avg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'precipitation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wind_speed': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wind_direction': forms.Select(attrs={'class': 'form-control'}),
            'pressure': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'visibility': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weather_condition': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        temp_max = cleaned_data.get('temperature_max')
        temp_min = cleaned_data.get('temperature_min')
        if temp_max is not None and temp_min is not None and temp_max < temp_min:
            raise ValidationError("Maximum temperature cannot be less than minimum temperature.")
        return cleaned_data


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV File',
        help_text='Required columns: date, city, temperature_max, temperature_min, temperature_avg, humidity, precipitation, wind_speed',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )
    REQUIRED_COLUMNS = ['date', 'city', 'temperature_max', 'temperature_min', 'temperature_avg', 'humidity', 'precipitation', 'wind_speed']

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise ValidationError("Please upload a CSV file.")
        if csv_file.size > 10 * 1024 * 1024:
            raise ValidationError("File size must be under 10MB.")
        try:
            df = pd.read_csv(csv_file)
            missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns.str.lower())
            if missing_columns:
                raise ValidationError(f"Missing required columns: {', '.join(missing_columns)}")
            df.columns = df.columns.str.lower().str.strip()
            df['date'] = pd.to_datetime(df['date']).dt.date
            csv_file.seek(0)
        except pd.errors.EmptyDataError:
            raise ValidationError("The uploaded file is empty.")
        except Exception as e:
            if 'Missing required columns' in str(e):
                raise
            raise ValidationError(f"Error reading CSV file: {str(e)}")
        return csv_file


class SearchFilterForm(forms.Form):
    city = forms.ChoiceField(choices=[('', 'All Cities')] + WeatherData.CITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    temp_min = forms.FloatField(required=False, label='Min Temp (C)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min temp'}))
    temp_max = forms.FloatField(required=False, label='Max Temp (C)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max temp'}))
    sort_by = forms.ChoiceField(choices=[
        ('-date', 'Date (Newest)'), ('date', 'Date (Oldest)'), ('city', 'City (A-Z)'),
        ('-city', 'City (Z-A)'), ('-temperature_avg', 'Temp (High-Low)'), ('temperature_avg', 'Temp (Low-High)'),
    ], required=False, initial='-date', widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise ValidationError("Start date cannot be after end date.")
        return cleaned_data
