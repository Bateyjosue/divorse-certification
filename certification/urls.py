from django.urls import path, include
from .views import IndexView, DashboardView, AddCoupleView

app_name = 'certification'
urlpatterns=[
    path('', IndexView.as_view(), name='home'),
    path('dash', DashboardView.as_view(), name='dashboard'),
    path('add-couple', AddCoupleView.as_view(), name='add-couple'),
]