from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import CoupleForm, WedForm, DivorseForm, UserForm, FindForm
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
import json
from django.http import JsonResponse

from xhtml2pdf import pisa 
from django.template.loader import get_template

from django.core.mail import send_mail

from django.contrib.auth import get_user_model
from django.conf import settings

from .filters import WedFilter, CoupleFilter, DivorseFilter

User = get_user_model()
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request,'index.html')

class SearchDocumentView(View):
    pass
def searchCertificate(request):
    if request.method == 'GET':
        cert = request.GET.get('certificates-category')
        search = Wed.objects.filter(wed_matricule = request.GET.get('search'))
        search_divorse = Divorse.objects.filter(divorse_matricule = request.GET.get('search')) 
        context ={
            'wed' : search,
            'divorse': search_divorse,
            'CERTIFICATE' : cert,
        }
        return render(request,'search-doc.html', context)

class RenderCertificate(View):
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
class CertificateView(View):
    def get(self, request, pk):
        if Divorse.objects.filter(pk = pk).exists():
            if Divorse.objects.filter(pk =pk, payment = True):
                template_path = 'certificate.html'
                divorse = Divorse.objects.filter(divorse_matricule = pk)
                context = {
                    'divorse' : divorse,
                } 
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename='+pk+'.pdf'
                template = get_template(template_path)
                html = template.render(context)
                pisa_status = pisa.CreatePDF(html, dest=response )

                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            else:
                context = {
                    'pk' : pk,
                }
                return render(request, 'payment.html', context)
        elif Wed.objects.filter(pk = pk).exists():
            if Wed.objects.filter(pk = pk, payment = True):
                template_path = 'certificate.html'
                wed = Wed.objects.filter(wed_matricule = pk)
                context = {
                    'wed' : wed,
                } 
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'filename='+pk+'.pdf'
                template = get_template(template_path)
                html = template.render(context)
                pisa_status = pisa.CreatePDF(html, dest=response )
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            else:
                context = {
                    'pk' : pk,
                }
                return render(request, 'payment.html', context)

class PaymentView(View):
    def get(self, request):
        return render(request, 'payment.html')
    
def updateStatus(request):
    data = json.loads(request.body)
    certId = data['id']
    status = data['status']
    if Wed.objects.get(pk = certId).exists():
        Wed.objects.filter(pk=certId).update(payment=True)
    else:
        Divorse.objects.filter(pk=certId).update(payment=True)
    return JsonResponse('Certificate id update', safe=False)
class DashboardView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wed = Wed.objects.all()
            context = {
                'couple': Couple.objects.all(),
                'wed': wed,
                'wed_filter' : WedFilter(request.GET, Wed.objects.all()),
                'divorse': Divorse.objects.all(),
                'couple_count':Couple.objects.all().count(),
                'wed_count':Wed.objects.all().count(),
                'divorse_count':Divorse.objects.all().count(),
                'user_count':User.objects.all().count(),
            }
            return render(request,'dashboard.html', context)
        else:
            return redirect('account_login')
class AddCoupleView(CreateView):
    model = Couple
    form_class = CoupleForm
    template_name = 'add-couple.html'
    sucess_message = 'Added'
    error_message = 'Error :: Not saved'
    success_url = reverse_lazy('certification:dashboard')

class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profil.html'
    success_message = 'Updated'
    success_url = reverse_lazy('certification:dashboard')
class AddWedView(View):
    def get(self, request):
        context ={
            'wed' : WedForm(),
        }
        return render(request,'add-wed.html',context)
    def post(self, request):
        messageSent = False
        cou = Couple.objects.filter(pk = request.POST.get('couple'))
        wed = WedForm(request.POST)
        if wed.is_valid():
            couple = request.POST.get('couple')
            wed_matricule = request.POST.get('wed_matricule')
            couples = Wed.objects.filter(couple_id = couple)
            if not Wed.objects.filter(couple_id=couple).exists():
                wed.save(commit=True)
                send_mail(
                    'Marriage confirmation',
                    str(Wed.objects.get(couple_id=couple)) + ' is your certificate matricule',
                    settings.DEFAULT_FROM_EMAIL,
                    ['josuebatey19@gmail.com'],
                    fail_silently=False,
                )
                messageSent = True
                print('Id Couple ' + couple)
                print(cou) 
                print(couples)
                messages.success(request, ' Saved ')
                return HttpResponseRedirect(reverse('certification:add-wed'))
            else:
                print (couple)
                if Wed.objects.get(couple = couple).couple.groom_status and Wed.objects.get(couple = couple).couple.bride_status:
                    wed.save(commit=True)
                    send_mail(
                        'Marriage confirmation',
                        request.POST.get('wed_matricule') + ' is your certificate matricule',
                        'josuebatey19@gmail.com',
                        ['josuebatey19@gmail.com'],
                        fail_silently=False,
                    )
                    messages.success(request, ' Saved ')
                    return HttpResponseRedirect(reverse('certification:dashboard'))
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
            send_mail(
                'Divorse Certificate confirmation',
                str(Divorse.objects.get(wed=weds)) + ' is your certificate matricule',
                settings.DEFAULT_FROM_EMAIL,
                ['josuebatey19@gmail.com'],
                fail_silently=False,
            )
            couple = request.POST.get('couple')
            if Wed.objects.filter(wed_matricule = weds).exists():
                Wed.objects.filter(wed_matricule = weds).update(is_divorsed= True)
                Couple.objects.filter(pk = couple).update(bride_status= True, groom_status= True)
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

class FindView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form' : FindForm()
        }
        return render(request, 'find.html', context)
    def post(self, request):
        form  = FindForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request has been sent')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Request has not been sent')
            return HttpResponseRedirect('./')