# apps/service_requests/urls.py
from django.urls import path
from . import views

app_name = 'service_requests'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.create_request, name='create_request'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/update/', views.request_update, name='request_update'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
]