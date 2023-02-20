from rest_framework import generics, status, mixins
from django_filters.rest_framework import DjangoFilterBackend
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


class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
