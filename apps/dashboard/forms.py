# apps/dashboard/forms.py
from django import forms
from apps.service_requests.models import ServiceRequest

class ServiceRequestFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + list(ServiceRequest.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'All')] + list(ServiceRequest.PRIORITY_CHOICES)

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
