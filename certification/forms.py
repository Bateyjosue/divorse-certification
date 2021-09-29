from django import forms
from django.forms import fields
from .models import Couple, Wed, Divorse

class CoupleForm(forms.ModelForm):
    class Meta:
        model = Couple
        exclude = ['created_at', 'updated_at']

class WedForm(forms.ModelForm):
    class Meta:
        model = Wed
        exclude = ['created_at', 'updated_at', 'is_divorsed']

class DivorseForm(forms.ModelForm):
    class Meta:
        model = Divorse
        exclude = ['created_at', 'updated_at']