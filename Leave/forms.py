from django import forms
from .models import LeaveRequest

class LeaverequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields  = ['leave_type','from_date','to_date','reason']
        