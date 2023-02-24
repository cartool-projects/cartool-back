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
    readonly_fields = ('slug', 'views')
    list_display = ('name', 'price', 'discount', 'get_categories')
    list_filter = ('discount', 'category', 'price')
    search_fields = ('name', 'description')
    sortable = 'order'
    list_per_page = 10

    def get_categories(self, obj):
        if obj.category:
            return obj.category.get_path()
        return None

    get_categories.short_description = 'Category Hierarchy'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'category_hierarchy')
    readonly_fields = ('slug',)
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    sortable = 'order'
    list_per_page = 10

    def category_hierarchy(self, obj):
        return obj.get_path()

    category_hierarchy.short_description = 'Category Hierarchy'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register([Order, ProductImage, Discount, Payment])
admin.site.register([Cart, ProductSpecs], SortableAdmin)
