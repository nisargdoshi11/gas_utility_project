# apps/service_requests/admin.py
from django.contrib import admin
from .models import ServiceRequest, RequestComment

class RequestCommentInline(admin.TabularInline):
    model = RequestComment
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_type', 'customer', 'status', 'priority', 'created_at', 'assigned_to')
    list_filter = ('status', 'request_type', 'priority', 'created_at')
    search_fields = ('customer__email', 'description', 'resolution_notes')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RequestCommentInline]
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('customer', 'request_type', 'priority', 'status')
        }),
        ('Request Details', {
            'fields': ('description', 'attachment', 'assigned_to')
        }),
        ('Resolution', {
            'fields': ('resolution_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )