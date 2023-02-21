from django.utils import timezone
from rest_framework import generics, status, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer, SpecsSerializer, \
    ProductImageSerializer, ProductRetrieveSerializer
from cartool.utils.serializer_factory import SerializerFactory
from .filters import ProductFilterBackend, ProductFilter


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Product.objects.select_related('discount') \
        .prefetch_related('product_image',
                          'category',
                          'product_specs',
                          )
    filter_backends = [DjangoFilterBackend, ProductFilterBackend]
    filterset_class = ProductFilter

    serializer_class = SerializerFactory(
        list=ProductSerializer,
        retrieve=ProductRetrieveSerializer,
        default=ProductSerializer
    )

    @action(detail=False, methods=['get'])
    def discounted_products(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(discount__isnull=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def increase_views(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.increase_views()
        return Response({'message': 'Views increased'}, status=status.HTTP_200_OK)

    def get_filtered_queryset(self, queryset, filter_criteria):
        queryset = self.filter_queryset(queryset).filter(**filter_criteria)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Refactor existing methods to use the helper method
    @action(detail=False, methods=['get'])
    def most_viewed(self, request):
        queryset = self.get_queryset().order_by('-views')
        return self.get_filtered_queryset(queryset, {})

    @action(detail=False, methods=['get'])
    def new_product(self, request):
        five_days_ago = timezone.now() - timezone.timedelta(days=14)
        queryset = self.get_queryset().filter(created_at__gte=five_days_ago)
        return self.get_filtered_queryset(queryset, {})

    @action(detail=False, methods=['get'])
    def popular(self, request):
        return self.get_filtered_queryset(self.get_queryset(), {'popular': True})

    @action(detail=False, methods=['get'])
    def with_free_delivery(self, request):
        return self.get_filtered_queryset(self.get_queryset(), {'free_delivery': True})


class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
