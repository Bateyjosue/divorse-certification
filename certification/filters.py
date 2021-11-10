import django_filters
from .models import Wed, Couple, Divorse

class WedFilter(django_filters.FilterSet):
    wed_matricule = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Wed
        fields = ['wed_matricule', 'couple']

class CoupleFilter(django_filters.FilterSet):
    class Meta:
        model = Couple
        fields = ['groom_full_name', 'bride_full_name', 'groom_mail', 'bride_mail']

class DivorseFilter(django_filters.FilterSet):
    class Meta:
        model = Divorse
        fields = ['wed']