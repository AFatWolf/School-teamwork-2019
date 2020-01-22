from django import forms
from .models import *

class UploadEventImageForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['cover_image']