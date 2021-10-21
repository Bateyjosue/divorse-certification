from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Wed, Couple,Divorse, Payment
# Register your models here.
@admin.register(Wed)
class WedAdmin(admin.ModelAdmin):
    fields =[]
    list_display = ('pk', 'couple','term', 'place', 'officer', 'is_divorsed')


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    fields =[]
    list_display = ('pk','groom_Nat_ID', 'groom_full_name', 'groom_dob','groom_phone','groom_photo','groom_mail','groom_address','groom_status',
    'bride_Nat_ID', 'bride_full_name', 'bride_dob','bride_phone','bride_mail','bride_address','bride_status','created_at','updated_at')


@admin.register(Divorse)
class DivorseAdmin(admin.ModelAdmin):
    fields =['divorse_matricule', 'wed','sentence']
    list_display = ('pk','divorse_matricule', 'wed','sentence', 'created_at', 'updated_at')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['services', 'price', 'transaction_number', 'transaction_name','Divorse', 'mariage' ]