from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import CoupleForm, WedForm, DivorseForm, PaymentForm, UserForm
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy

from xhtml2pdf import pisa 
from django.template.loader import get_template

from django.core.mail import send_mail

from django.contrib.auth import get_user_model

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
        if Payment.objects.filter(Divorse = pk).exists() or Payment.objects.filter(mariage = pk).exists():
            d= Payment.objects.filter(Divorse = pk)
            m = Payment.objects.filter(mariage = pk)
            # if d.is_done or m.is_done:
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
        return redirect('certificates/payment')
class PaymentView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment.html'
    sucess_message = 'Added'
    error_message = 'Error :: Not saved'
    # redirect('dashboard')

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

# class AddCoupleView(View):
#     def get(self, request):
#         context = {
#             'couple': CoupleForm(),
#         }
#         return render(request,'add-couple.html', context)

#     def post(self, request):
#         couple = CoupleForm(request.POST)
#         # bride = CoupleForm(request.POST)
#         if  couple.is_valid():
#             couple.save(commit=True)
#             messages.success(request, 'Data saved successfully')
#             # if bride.is_valid():
#             #     bride.save(commit=True)
#             #     messages.success(request, 'Data saved successfully [bride]')
#             # else:
#             #     messages.success(request, 'Check Information provided in Bride')
#             #     return HttpResponseRedirect(reverse('certification:add-couple'))
#             return HttpResponseRedirect(reverse('certification:dash'))
#         else:
#             messages.success(request, 'Check Information provided')
#             return HttpResponseRedirect(reverse('certification:add-couple'))

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
    # def get(self, request, pk):
    #     context = {
    #             'form': UserForm(request.GET, instance = request.user)
    #         }
    #     return render(request, 'profil.html', context)
    # def POST(self, request, pk):
    #     form_class = UserForm(request.POST, instance = request.user)
    #     if form_class.is_valid():
    #         form_class.save()
    #         messages.success(request, ' Successfully')
    #         return redirect(to = 'dashboard')
    #     else:
    #         messages.success(request, ' Not Save')
    #         return redirect(to = 'profile')
        # template_name = 'profil.html'
        # return HttpResponseRedirect(reverse('dashboard'))

#     def get(self, request):
#         context = {
#             'couple': CoupleForm(),
#         }
#         return render(request,'add-couple.html', context)

#     def post(self, request):
#         couple = CoupleForm(request.POST)
#         # bride = CoupleForm(request.POST)
#         if  couple.is_valid():
#             couple.save(commit=True)
#             messages.success(request, 'Data saved successfully')
#             # if bride.is_valid():
#             #     bride.save(commit=True)
#             #     messages.success(request, 'Data saved successfully [bride]')
#             # else:
#             #     messages.success(request, 'Check Information provided in Bride')
#             #     return HttpResponseRedirect(reverse('certification:add-couple'))
#             return HttpResponseRedirect(reverse('certification:dash'))
#         else:
#             messages.success(request, 'Check Information provided')
#             return HttpResponseR

class AddWedView(View):
    def get(self, request):
        context ={
            'wed' : WedForm(),
        }
        return render(request,'add-wed.html',context)
    def post(self, request):
        cou = Couple.objects.filter(pk = request.POST.get('couple'))

        wed = WedForm(request.POST)
        if wed.is_valid():
            couple = request.POST.get('couple')
            couples = Wed.objects.filter(couple=couple)
            if not Wed.objects.filter(couple=couple).exists():
                # if couples.couple.groom_status == 'Divorse' and couples.bride_status == 'Divorse':
                wed.save(commit=True)
               
                couples.couple.groom_status.update(groom_status='Married')
                Couple.objects.filter(pk = couple).update(groom_status='Married')
                messages.success(request, ' Saved ')
                send_mail(
                    'Marriage comfirmation',
                    request.POST.get('wed_matricule') + ' is your certificate matricule',
                    'josuebatey19@gmail.com',
                    [request.POST.get('wed').couple.groom_mail, 'josuebatey19@gmail.com'],
                    fail_silently=False,
                )
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
            couple = request.POST.get('couple')
            if Wed.objects.filter(wed_matricule = weds).exists():
                Wed.objects.filter(wed_matricule = weds).update(is_divorsed= True)
                Couple.objects.filter(pk = couple).update(bride_status= True, groom_status= True)
                # Wed.objects.filter(wed_matricule = weds).update(weds.)
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

