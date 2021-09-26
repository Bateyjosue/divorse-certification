from django.shortcuts import redirect, render
from django.views import View
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request,'index.html')

class DashboardView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,'dashboard.html')
        else:
            redirect('account_login')