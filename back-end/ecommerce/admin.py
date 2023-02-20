from django.contrib import admin
from adminsortable.admin import SortableAdmin

from .models import Product, Order, ProductSpecs, ProductImage, Category, Discount, Cart, Payment


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSpecsInline(admin.TabularInline):
    model = ProductSpecs


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSpecsInline]
    readonly_fields = ('slug',)
    list_display = ('name', 'price', 'discount', 'get_categories', 'slug')
    list_filter = ('discount', 'category', 'price')
    search_fields = ('name', 'description')
    sortable = 'order'

    def get_categories(self, obj):
        return ', '.join([category.name for category in obj.category.all()])

    def save_model(self, request, obj, form, change):
        obj.slug = obj.name.replace(' ', '-').lower()
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
admin.site.register([Order, ProductImage, Category, Discount, Payment])
admin.site.register([Cart, ProductSpecs], SortableAdmin)
