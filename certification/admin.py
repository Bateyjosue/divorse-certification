from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Wed, Couple,Divorse
# Register your models here.
@admin.register(Wed)
class WedAdmin(admin.ModelAdmin):
    fields =[]
    list_display = ('pk', 'bride', 'groom','term', 'place', 'officer', 'is_divorsed')


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    fields =[]
    list_display = ('Nat_ID', 'full_name', 'dob','phone','mail','address','status','created_at','updated_at')


@admin.register(Divorse)
class DivorseAdmin(admin.ModelAdmin):
    fields =['divorse_matricule', 'wed','sentence']
    list_display = ('pk','divorse_matricule', 'wed','sentence', 'created_at', 'updated_at')