from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request,'index.html')

class DashboardView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'couple': Couple.objects.all(),
                'wed': Wed.objects.all(),
                'divorse': Divorse.objects.all(),
                'couple_count':Couple.objects.all().count(),
                'wed_count':Wed.objects.all().count(),
                'divorse_count':Divorse.objects.all().count(),
            }
            return render(request,'dashboard.html', context)
        else:
            return redirect('account_login')

class AddCoupleView(View):
    def get(self, request):
        context = {
            'groom': CoupleForm(),
            'bride': CoupleForm(),
        }
        return render(request,'add-couple.html', context)
    def post(self, request):
        pass

class AddWedView(View):
    def get(self, request):
        context ={
            'wed' : WedForm(),
        }
        return render(request,'add-wed.html',context)

class AddDivorseView(View):
    def get(self, request):
        context ={
            'divorse' : DivorseForm(),
            
        }
        return render(request,'add-divorse.html',context)