from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy

from .cart import Cart
from store.models import Product


def cart_summary(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'store/cart/summary.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart_qty})
        return response


def cart_remove(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)
        cart_qty = cart.__len__()
        cart_total_price = cart.get_total_price()
        response = JsonResponse({'cart_qty': cart_qty, 'cart_total_price': cart_total_price})
        return response


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        updated_qty = int(request.POST.get('updated_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, updated_qty=updated_qty)
        cart_qty=cart.__len__()
        cart_total_price=cart.get_total_price()
        response = JsonResponse({'cart_qty': cart_qty,'cart_total_price':cart_total_price})
        return response
