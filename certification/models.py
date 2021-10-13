from django.db import models
from django.db.models.expressions import Value
from django.db.models.fields import DateTimeField

from django.db.models.signals import pre_save
from core.utils import *
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser:



class Couple(models.Model):
    groom_Nat_ID = models.CharField(max_length=20,blank=False,null=False, unique=False)
    groom_full_name = models.CharField(max_length=50)
    groom_dob = models.DateTimeField(blank=True, null=True)
    groom_phone = models.CharField(max_length=50, unique=True)
    groom_mail = models.EmailField(max_length=50, unique=True)
    groom_photo = models.ImageField(upload_to='couple_images/')
    groom_address = models.CharField(max_length=200)
    choice_status = (('Pending', 'Pending'), ('Married', 'Married'), ('Divorse', 'Divorse'))
    groom_status = models.CharField(max_length=50,choices=choice_status, default=('Pending'))

    bride_Nat_ID = models.CharField(max_length=20,blank=False,null=False, unique=False)
    bride_full_name = models.CharField(max_length=50)
    bride_dob = models.DateTimeField(blank=True, null=True)
    bride_phone = models.CharField(max_length=50, unique=True)
    bride_mail = models.EmailField(max_length=50, unique=True)
    bride_photo = models.ImageField(upload_to='couple_images/')
    bride_address = models.CharField(max_length=200)
    choice_status = (('Pending', 'Pending'), ('Married', 'Married'), ('Divorse', 'Divorse'))
    bride_status = models.CharField(max_length=50,choices=choice_status, default=('Pending'))

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.groom_Nat_ID + '/'+self.bride_Nat_ID 

class Wed(models.Model):
    wed_matricule = models.CharField(max_length=50,primary_key=True, null=False, blank=True)
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE)
    term =  models.CharField(max_length=200)
    place = models.CharField(max_length=200,help_text="DRC/KINSHASA/GOMBE")
    officer = models.CharField(max_length=200,help_text="Officer full-name")
    is_divorsed = models.BooleanField(default=False)

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
    divorse_matricule =models.CharField(max_length=50,primary_key=True)
    wed = models.OneToOneField(Wed, on_delete=models.CASCADE, unique=True)
    sentence = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.divorse_matricule

    def get_Divorse_matricule(self):
        pass
def pre_save_divorse_matricule(sender, instance, *args, **kwargs):
    if not instance.divorse_matricule:
        instance.divorse_matricule =unique_divorse_matricule(instance)

pre_save.connect(pre_save_divorse_matricule, sender=Divorse)