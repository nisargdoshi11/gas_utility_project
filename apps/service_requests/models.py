# apps/service_requests/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    REQUEST_TYPES = [
        ('gas_leak', 'Gas Leak'),
        ('connection', 'New Connection'),
        ('billing', 'Billing Issue'),
        ('maintenance', 'Maintenance'),
        ('meter_reading', 'Meter Reading'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    request_type = models.CharField(
        _("Request Type"),
        max_length=20,
        choices=REQUEST_TYPES
    )
    priority = models.CharField(
        _("Priority"),
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    description = models.TextField(_("Description"))
    attachment = models.FileField(
        _("Attachment"),
        upload_to='service_requests/',
        blank=True,
        null=True
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolution_notes = models.TextField(_("Resolution Notes"), blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Service Request")
        verbose_name_plural = _("Service Requests")

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.customer.email} - {self.status}"

class RequestComment(models.Model):
    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"Comment by {self.user.email} on {self.request}"