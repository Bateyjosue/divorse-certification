from django.urls import path, include
from .views import searchCertificate, IndexView, DashboardView, AddCoupleView, AddWedView, AddDivorseView, SearchDocumentView, CertificateView

app_name = 'certification'
urlpatterns=[
    path('', IndexView.as_view(), name='home'),
    path('search', searchCertificate, name='search'),
    path('certificate/<str:pk>', CertificateView.as_view(), name='certificates'),
    path('dash', DashboardView.as_view(), name='dashboard'),
    path('add-couple', AddCoupleView.as_view(), name='add-couple'),
    path('add-wed', AddWedView.as_view(), name='add-wed'),
    path('add-divorse', AddDivorseView.as_view(), name='add-divorse'),
]