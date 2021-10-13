from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import CoupleForm, WedForm, DivorseForm
from django.contrib import messages
from django.urls import reverse

from xhtml2pdf import pisa 
from django.template.loader import get_template
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request,'index.html')

class SearchDocumentView(View):
    pass
def searchCertificate(request):
    if request.method == 'GET':
        cert = request.GET.get('certificates-category')
        # if  CERTIFICATE == 'Weddings':
        search = Wed.objects.filter(wed_matricule = request.GET.get('search'))
        # search_divorse = None
        # elif  CERTIFICATE == 'Divorse':
        search_divorse = Divorse.objects.filter(divorse_matricule = request.GET.get('search')) 
        # search = None
        context ={
            'wed' : search,
            'divorse': search_divorse,
            'CERTIFICATE' : cert,
        }
        return render(request,'search-doc.html', context)

class CertificateView(View):
    def get(self, request, pk):
        template_path = 'certificate.html'
        wed = Wed.objects.filter(wed_matricule = pk)
        divorse = Divorse.objects.filter(divorse_matricule = pk)
        context = {
            'wed': wed,
            'divorse': divorse
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename='+pk+'.pdf'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response )

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

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
            'couple': CoupleForm(),
        }
        return render(request,'add-couple.html', context)

    def post(self, request):
        couple = CoupleForm(request.POST)
        # bride = CoupleForm(request.POST)
        if  couple.is_valid():
            couple.save(commit=True)
            messages.success(request, 'Data saved successfully')
            # if bride.is_valid():
            #     bride.save(commit=True)
            #     messages.success(request, 'Data saved successfully [bride]')
            # else:
            #     messages.success(request, 'Check Information provided in Bride')
            #     return HttpResponseRedirect(reverse('certification:add-couple'))
            return HttpResponseRedirect(reverse('certification:dash'))
        else:
            messages.success(request, 'Check Information provided')
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
            couple = request.POST.get('couple')
            couples = Wed.objects.filter(couple=couple)
            if not Wed.objects.filter(couple=couple).exists():
                # if couples.couple.groom_status == 'Divorse' and couples.bride_status == 'Divorse':
                wed.save(commit=True)
                couples.couple.groom_status.update(groom_status='Married')
                Couple.objects.filter(groom_Nat_ID = couple).update(groom_status='Married')
                messages.success(request, ' Saved ')
                return HttpResponseRedirect(reverse('certification:dashboard'))
                # else:
                #     messages.success(request, 'Data Not Found')
                #     return HttpResponseRedirect(reverse('certification:add-wed'))
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

