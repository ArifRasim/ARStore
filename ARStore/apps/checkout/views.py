import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from paypalcheckoutsdk.orders import OrdersGetRequest

# Create your views here.
from ARStore.apps.accounts.models import Address
from ARStore.apps.cart.cart import Cart
from ARStore.apps.checkout.models import DeliveryOptions
from ARStore.apps.orders.models import OrderItem, Order
from .paypal import PayPalClient


class DeliveryOptionsView(LoginRequiredMixin, ListView):
    model = DeliveryOptions
    template_name = 'checkout/delivery_options.html'
    context_object_name = 'delivery_options'

    def get_queryset(self):
        qs = super(DeliveryOptionsView, self).get_queryset()
        return qs.filter(is_active=True)


@login_required
def cart_update_delivery(request):
    cart = Cart(request)
    delivery_option = request.POST.get('delivery_option')
    delivery_type = get_object_or_404(DeliveryOptions, id=delivery_option)
    cart_updated_price = cart.cart_update_delivery(delivery_type.delivery_price)

    session = request.session

    session['purchase'] = {
        'delivery_id': delivery_type.id
    }
    session.modified = True
    response = JsonResponse({'total': cart_updated_price, 'delivery_price': delivery_type.delivery_price})
    return response


@login_required
def delivery_address(request):
    delivery_addresses = Address.objects.filter(customer=request.user).order_by('-default')

    if 'purchase' not in request.session:
        messages.success(request, 'Choose a delivery option')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if not delivery_addresses:
        messages.success(request, 'Add an address for delivery', {'yes'})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if 'address' not in request.session:
        request.session['address'] = {'address_id': str(delivery_addresses[0].id)}
    else:
        request.session['address']['address_id'] = str(delivery_addresses[0].id)
    return render(request, 'checkout/delivery_address.html', {'addresses': delivery_addresses})


@login_required
def payment_selection(request):
    if 'address' not in request.session:
        messages.success(request, 'Please select an address')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'checkout/payment_selection.html')


@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'checkout/payment_successful.html', {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)

    cart = Cart(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in cart:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)
