from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # FIXED: Changed send_verification_email to verify_email_view
    path('verify/<uidb64>/<token>/', views.verify_email_view, name='verify_email'),
    path('verification-sent/', views.verification_sent_view, name='verification_sent'),
    path('verification-success/', views.verification_success_view, name='verification_success'),
    path('verification-failed/', views.verification_failed_view, name='verification_failed'),
]