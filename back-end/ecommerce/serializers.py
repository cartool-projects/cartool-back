from rest_framework import serializers

from .models import Product, Discount, Category, ProductSpecs



class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name',)


class SpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecs
        exclude = ['order', 'product']


class ProductSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')
    product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'discount', 'product_image', 'status', 'free_delivery')


class ProductRetrieveSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(read_only=True)
    product_image = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    product_specs = SpecsSerializer(many=True, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Product
        fields = '__all__'

