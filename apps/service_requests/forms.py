# apps/service_requests/forms.py
from django import forms
from .models import ServiceRequest, RequestComment

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'priority', 'description', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'assigned_to', 'resolution_notes']
        widgets = {
            'resolution_notes': forms.Textarea(attrs={'rows': 3}),
        }
