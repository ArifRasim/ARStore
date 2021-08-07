from django.contrib import admin
from django.contrib.admin import TabularInline
from mptt.admin import MPTTModelAdmin

from ARStore.apps.store.models import Category, ProductSpecification, ProductType, ProductImage, \
    ProductSpecificationValue, Product

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline
    ]
