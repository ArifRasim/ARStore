from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from ARStore.apps.store.models import Product
from .cart import Cart


# Create your views here.
class CartView(TemplateView):
    template_name = 'store/cart/summary.html'
    model = Cart
    context_object_name = 'cart'


def cart_add(request):
    cart = Cart(request)
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, qty=product_qty)
    cart_qty = cart.__len__()
    response = JsonResponse({'qty': cart_qty})
    return response


def cart_remove(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    cart_qty = cart.__len__()
    cart_total_price = cart.get_total_price()
    response = JsonResponse({'cart_qty': cart_qty, 'cart_total_price': cart_total_price})
    return response


def cart_update(request):
    cart = Cart(request)

    product_id = int(request.POST.get('product_id'))
    updated_qty = int(request.POST.get('updated_qty'))
    product = get_object_or_404(Product, id=product_id)
    cart.update(product=product, updated_qty=updated_qty)
    cart_qty = cart.__len__()
    cart_total_price = cart.get_total_price()
    response = JsonResponse({'cart_qty': cart_qty, 'cart_total_price': cart_total_price})
    return response
