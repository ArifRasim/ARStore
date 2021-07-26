from django.contrib import admin
# # Register your models here.
# from store.models import Product, Category
#
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'slug', 'price', 'in_stock', 'created_at', 'updated_at']
#     list_filter = ['in_stock', 'is_active']
from django.contrib.admin import TabularInline
from mptt.admin import MPTTModelAdmin

from store.models import Category, ProductSpecification, ProductType, ProductImage, ProductSpecificationValue, Product

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
