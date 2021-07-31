import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient
# Create your views here.
from accounts.models import Address
from cart.cart import Cart
from checkout.models import DeliveryOptions
from orders.models import OrderItem, Order


@login_required
def delivery_options(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    return render(request, 'checkout/delivery_options.html', {'delivery_options': delivery_options})


@login_required
def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':
        delivery_option = request.POST.get('delivery_option')
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        cart_updated_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session

        if 'purchase' in session:
            session['purchase']['delivery_id'] = delivery_type.id
        else:
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
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if 'address' not in request.session:
        request.session['address'] = {'address_id': str(delivery_addresses[0].id)}
    else:
        request.session['address']['address_id'] = str(delivery_addresses[0].id)
    return render(request, 'checkout/delivery_address.html', {'addresses': delivery_addresses})


@login_required
def payment_selection(request):
    if 'address' not in request.session:
        messages.success(request, 'Please select and address')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'checkout/payment_selection.html')


@login_required
def payment_successful(request):
    cart=Cart(request)
    cart.clear()
    return render(request, 'checkout/payment_successful.html',{})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)

    total_paid = response.result.purchase_units[0].amount.value

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