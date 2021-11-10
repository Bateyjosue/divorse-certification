from django.db import models
from django.db.models.expressions import Value
from django.db.models.fields import DateTimeField

from django.db.models.signals import pre_save
from django.http import request
from core.utils import *
from django.urls import reverse
from django_countries.fields import CountryField


# Create your models here.
# class User(User):
#     def get_absolute_url(self):
#         return reverse('dashboard')


# class User(AbstractUser):
#     gender = (
#         ('O', 'Others'),
#         ('M', 'Male'),
#         ('F', 'Female')
#     )
#     sex         = models.CharField(max_length=10, choices =gender, default='Others')
#     picture     = models.ImageField(upload_to='profile/', null=False, blank=False)
#     phone        = models.CharField(max_length=255, default='(000) 000 000 000')
#     city        = models.CharField(max_length=255)
#     district    = models.CharField(max_length=255, default='Kicukiro')

#     def __str__(self):
#         return self.username

class Couple(models.Model):
    groom_Nat_ID = models.CharField(max_length=20,blank=False,null=False, unique=False)
    groom_full_name = models.CharField(max_length=50)
    groom_dob = models.DateTimeField(blank=True, null=True)
    groom_phone = models.CharField(max_length=50, unique=True)
    groom_mail = models.EmailField(max_length=50, unique=True)
    groom_photo = models.ImageField(upload_to='couple_images/', default='static/images/avatar-profil.png')
    groom_address = models.CharField(max_length=200)
    # choice_status = (('Pending', 'Pending'), ('Married', 'Married'), ('Divorse', 'Divorse'))
    groom_status = models.BooleanField(default=False)

    bride_Nat_ID = models.CharField(max_length=20,blank=False,null=False, unique=False)
    bride_full_name = models.CharField(max_length=50)
    bride_dob = models.DateTimeField(blank=True, null=True)
    bride_phone = models.CharField(max_length=50, unique=True)
    bride_mail = models.EmailField(max_length=50, unique=True)
    bride_photo = models.ImageField(upload_to='couple_images/', default='static/images/avatar-profil.png')
    bride_address = models.CharField(max_length=200)
    bride_status = models.BooleanField(default=False)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.groom_full_name + '/'+ self.bride_full_name 
    def get_absolute_url(self):
        return reverse('certification:dashboard')

class Find(models.Model):
    national_ID = models.CharField(max_length=50)
    full_name  = models.CharField(max_length=50)
    certifiate = (('Marriage','Marriage'),('Divorce', 'Divorce'))
    requests = models.CharField(max_length=50, choices = certifiate)
    email = models.EmailField(max_length=50) 

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.full_name

class Wed(models.Model):
    wed_matricule = models.CharField(max_length=50,primary_key=True, null=False, blank=True)
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE)
    term =  models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    officer = models.CharField(max_length=200,verbose_name="Officer full-name")
    is_divorsed = models.BooleanField(default=False)
    payment = models.BooleanField(default=False, verbose_name="Is-Paid")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wed_matricule 
    
    def get_Wed_matricule(self):
        pass

def pre_save_wed_matricule(sender, instance, *args, **kwargs):
    if not instance.wed_matricule:
        instance.wed_matricule =unique_wed_matricule(instance)
pre_save.connect(pre_save_wed_matricule, sender=Wed)


class Divorse(models.Model):
    divorse_matricule =models.CharField(max_length=50,primary_key=True, null=False, blank=True)
    wed = models.OneToOneField(Wed, on_delete=models.CASCADE, unique=True)
    sentence = models.BooleanField(default=False)
    magistrate = models.CharField(max_length=50, default="John Kayumbi")
    signature = models.ImageField(upload_to='signature/', default="static/images/signature.jpeg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False, verbose_name="Is-Paid")

    def __str__(self):
        return self.divorse_matricule

def pre_divorse(sender, instance, *args, **kwargs):
    if not instance.divorse_matricule:
        instance.divorse_matricule =unique_divorse_matricule(instance)

pre_save.connect(pre_divorse, sender=Divorse)


"""class Payment(models.Model):
    ser = (
        ('Divorse', 'Divorse'),
        ('Marriage', 'Marriage')
    )
    services = models.CharField(max_length=50,choices =ser, help_text="Marriage costs 10$ & Divorse costs 5$")
    price = models.IntegerField(default=10)
    transaction_date = models.DateTimeField(auto_now_add=True)
    Divorse = models.ForeignKey(Divorse, on_delete=models.CASCADE, null=True, blank=True)
    mariage = models.ForeignKey(Wed, on_delete=models.CASCADE, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.services

    def get_absolute_url(self):
        return '/'
"""