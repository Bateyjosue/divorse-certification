from django.urls import path, include
from .views import IndexView, DashboardView
urlpatterns=[
    path('', IndexView.as_view(), name='home'),
    path('dash', DashboardView.as_view(), name='dashboard')
]