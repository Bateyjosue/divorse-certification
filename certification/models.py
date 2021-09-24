from django.db import models
from django.db.models.expressions import Value

from django.db.models.signals import pre_save
from core.utils import *

# Create your models here.
class Couple(models.Model):
    Nat_ID = models.CharField(max_length=20,blank=False,null=False)
    full_name = models.CharField(max_length=50)
    dob = models.DateTimeField()
    phone = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    photo = models.ImageField(upload_to='couple_images/')
    address = models.CharField(max_length=200)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Nat_ID 

class Term (models.Model):
    nature = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nature


class Wed(models.Model):
    wed_matricule = models.CharField(max_length=50,primary_key=True, null=False, blank=True)
    bride = models.OneToOneField(Couple, on_delete=models.CASCADE, related_name='brides', unique=True)
    groom = models.OneToOneField(Couple, on_delete=models.CASCADE,related_name='grooms', unique=True)
    term = models.ForeignKey(Term,on_delete=models.CASCADE)
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

class Sentence(models.Model):
    sentence = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    judge = models.CharField(max_length=200, help_text="Full-name of the judge who who pronounce the sentence")
    place = models.CharField(max_length=50,help_text="Country/State/Disctrict or Town")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sentence

class Divorse(models.Model):
    divorse_matricule =models.CharField(max_length=50,primary_key=True)
    wed = models.ForeignKey(Wed, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

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