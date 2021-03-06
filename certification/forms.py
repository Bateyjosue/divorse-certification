from django import forms
from django.forms import fields
from .models import Couple, Wed, Divorse, Find

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User

# User = get_user_model()
# User.get_success_url(reverse('dashboard'))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['user_permissions','password','last_login','groups','created_at', 'updated_at']

class FindForm(forms.ModelForm):
    class Meta:
        model =  Find
        exclude = ['created_at', 'updated_at']


class CoupleForm(forms.ModelForm):
    # bride_photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-photo'}), required=True)
    # groom_photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-photo'}), required=True)
    class Meta:
        model = Couple
        exclude = ['created_at', 'updated_at']

class WedForm(forms.ModelForm):
    class Meta:
        model = Wed
        exclude = ['created_at', 'updated_at', 'is_divorsed', 'wed_matricule']

class DivorseForm(forms.ModelForm):
    class Meta:
        model = Divorse
        exclude = ['created_at', 'updated_at']

"""class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['transaction_date', 'is_done']"""