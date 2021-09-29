from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
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
        groom = CoupleForm(request.POST)
        bride = CoupleForm(request.POST)
        if groom.is_valid() and bride.is_valid():
            groom.save(commit=True)
            bride.save(commit=True)
            messages.success(request, 'Data saved successfully')
            return HttpResponseRedirect(reverse('certification:dash'))
        else:
            messages.success(request, 'Check Information provided if are correct')
            return HttpResponseRedirect(reverse('certification:add-couple'))

class AddWedView(View):
    def get(self, request):
        context ={
            'wed' : WedForm(),
        }
        return render(request,'add-wed.html',context)
    def post(self, request):
        wed = WedForm(request.POST)
        if wed.is_valid():
            gr = request.POST.get('groom')
            bd = request.POST.get('bride')
            if not Wed.objects.filter(groom=gr).exists() or not Wed.objects.filter(bride=bd).exists:
                if Wed.objects.filter(is_divorsed= True).exists:
                    wed.save(commit=True)
                    messages.success(request, ' Saved ')
                    return HttpResponseRedirect(reverse('certification:dashoard'))
                else:
                    messages.success(request, 'Unfinilized Divorse Process')
                    return HttpResponseRedirect(reverse('certification:add-wed'))
            else:
                messages.success(request, 'Unfinilized Divorse Process')
                return HttpResponseRedirect(reverse('certification:add-wed'))

class AddDivorseView(View):
    def get(self, request):
        context ={
            'divorse' : DivorseForm(),
            
        }
        return render(request,'add-divorse.html',context)
    def post(self, request):
        divorse = DivorseForm(request.POST)
        if divorse.is_valid():
            divorse.save(commit=True)
            weds = request.POST.get('wed')
            if Wed.objects.filter(wed_matricule = weds).exists():
                Wed.objects.filter(wed_matricule = weds).update(is_divorsed= True)
                messages.success(request, 'Saved')
                return HttpResponseRedirect(reverse('certification:dashboard'))
        else:
            weds = request.POST.get('wed')
            wedd = Divorse.objects.filter(wed=weds).exists()
            print(wedd)
            if Divorse.objects.filter(wed=weds).exists():
                messages.error(request, 'Wedding Matricule exists')
                return HttpResponseRedirect(reverse('certification:add-divorse'))
            messages.error(request, 'Not saved')
            return HttpResponseRedirect(reverse('certification:add-divorse'))

