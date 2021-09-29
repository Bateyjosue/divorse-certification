from django.urls import path, include
from .views import IndexView, DashboardView, AddCoupleView, AddWedView, AddDivorseView

app_name = 'certification'
urlpatterns=[
    path('', IndexView.as_view(), name='home'),
    path('dash', DashboardView.as_view(), name='dashboard'),
    path('add-couple', AddCoupleView.as_view(), name='add-couple'),
    path('add-wed', AddWedView.as_view(), name='add-wed'),
    path('add-divorse', AddDivorseView.as_view(), name='add-divorse'),
]