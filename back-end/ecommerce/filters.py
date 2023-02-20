from django.db.models import Q
from django_filters import rest_framework
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import FilterSet, filters
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend

from ecommerce.models import Product, Category
from ecommerce.choices import ProductStatus


class ProductFilter(FilterSet):
    status = filters.ChoiceFilter(label=_('Status'), choices=ProductStatus.choices)
    category = filters.ModelMultipleChoiceFilter(label=_('Category'), queryset=Category.objects.all())
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gt')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lt')
    free_delivery = filters.BooleanFilter(method='filter_free_delivery', lookup_expr='exact')
    on_discount = filters.BooleanFilter(method='filter_on_discount', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['status', 'category', 'min_price', 'max_price', 'free_delivery', 'on_discount']

    @staticmethod
    def filter_free_delivery(queryset, name, value):
        if value:
            return queryset.filter(free_delivery=True)
        return queryset.filter(Q(free_delivery=False) | Q(free_delivery__isnull=True))

    @staticmethod
    def filter_on_discount(queryset, name, value):
        if value:
            return queryset.filter(discount__isnull=False)
        return queryset.filter(discount__isnull=True)


class ProductFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_class = ProductFilter(request.GET, queryset=queryset)
        return filter_class.qs
