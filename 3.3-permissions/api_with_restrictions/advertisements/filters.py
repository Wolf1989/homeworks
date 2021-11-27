from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from django_filters.filters import ChoiceFilter, DateFromToRangeFilter, ModelChoiceFilter

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    creator = ModelChoiceFilter(queryset=User.objects.all())
    status = ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'creator']
