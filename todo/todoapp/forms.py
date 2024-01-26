from . models import task
from django import forms

class todoform(forms.ModelForm):

    class Meta:
        model=task
        fields=['Task','priority','date']

