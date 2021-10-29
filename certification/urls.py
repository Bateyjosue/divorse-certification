from django.urls import path, include
from .views import searchCertificate, FindView, UpdateUserView, IndexView, DashboardView, AddCoupleView, PaymentView, AddWedView, AddDivorseView, SearchDocumentView, CertificateView

app_name = 'certification'
urlpatterns=[
    path('', IndexView.as_view(), name='home'),
    path('search', searchCertificate, name='search'),
    path('certificate/<str:pk>', CertificateView.as_view(), name='certificates'),
    path('certificate/<str:pk>/payment', PaymentView.as_view(), name='payment'),
    path('dash', DashboardView.as_view(), name='dashboard'),
    path('add-couple', AddCoupleView.as_view(), name='add-couple'),
    path('add-wed', AddWedView.as_view(), name='add-wed'),
    path('add-divorse', AddDivorseView.as_view(), name='add-divorse'),
    path('profile/<pk>', UpdateUserView.as_view(), name='profile'),
    path('find', FindView.as_view(), name='find'),
]