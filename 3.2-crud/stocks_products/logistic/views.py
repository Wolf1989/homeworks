from django.db import backends
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class CustomSearchFilter(SearchFilter):
    
    def get_search_terms(self, request):
        # Для поиска можно использовать: ?products=, ?[search_param]=
        params = request.query_params.get('products', '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'title', 'description']
    ordering_fields = ['id', 'title']
    ordering = ['id']


class StockViewSet(ModelViewSet):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, CustomSearchFilter, OrderingFilter]
    filterset_fields = ['address', 'id']
    search_fields = ['products__id', 'products__title']
    ordering_fields = ['id', 'address']
    ordering = ['id']