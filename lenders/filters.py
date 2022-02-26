import django_filters

from lenders.models import Lender


class LenderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Lender
        fields = ['active']