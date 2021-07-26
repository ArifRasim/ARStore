import products as products
from django.shortcuts import render, get_object_or_404

# Create your views here.
from store.models import Product, Category


def all_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'store/products/product.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'store/categories/category.html', context)
