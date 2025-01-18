from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Default auth URLs
    path('dashboard/', include('apps.dashboard.urls')),  # Ensure this is correct
    path('service_requests/', include('apps.service_requests.urls')),
]
