from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.search_view, name='search'),
    path('visualizations/', views.visualizations_view, name='visualizations'),
    path('insights/', views.insights_view, name='insights'),
    path('reports/', views.reports_view, name='reports'),
    path('upload-data/', views.upload_data_view, name='upload_data'),
    path('data/', views.data_list_view, name='data_list'),
    path('data/create/', views.create_record_view, name='create_record'),
    path('data/update/<int:pk>/', views.update_record_view, name='update_record'),
    path('data/delete/<int:pk>/', views.delete_record_view, name='delete_record'),
    path('send-reports-now/', views.send_reports_now_view, name='send_reports_now'),
    path('refresh-data/', views.refresh_weather_data_view, name='refresh_data'),
]
