from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Customer URLs
    path('', views.dashboard_view, name='dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('statistics/', views.customer_statistics, name='customer_statistics'),
    
    # Staff URLs
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/statistics/', views.staff_statistics, name='staff_statistics'),
    path('staff/reports/', views.staff_reports, name='staff_reports'),
    
    # API endpoints for dashboard data
    path('api/request-summary/', views.request_summary, name='request_summary'),
    path('api/monthly-stats/', views.monthly_stats, name='monthly_stats'),  # Ensure this is correct
]
