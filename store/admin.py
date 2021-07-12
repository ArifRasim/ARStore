from django.contrib import admin

# Register your models here.
from store.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price', 'in_stock', 'created_at', 'updated_at']
    list_filter = ['in_stock', 'is_active']
