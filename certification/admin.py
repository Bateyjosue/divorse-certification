from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Wed, Couple,Divorse
# Register your models here.
@admin.register(Wed)
class WedAdmin(admin.ModelAdmin):
    fields =[]


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    fields =[]


@admin.register(Divorse)
class DivorseAdmin(admin.ModelAdmin):
    fields =[]