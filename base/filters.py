import django_filters
from .models import Donner, Location


class BloodFilter(django_filters.FilterSet):
    class Meta:
        model = Donner
        fields = {'bloodgroups': ['exact'], 'division': ['exact'], 'location': ['exact']}
        
        
