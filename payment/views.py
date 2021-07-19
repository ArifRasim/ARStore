import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from orders.views import payment_confirmation


@login_required
def cart_view(request):
    cart = Cart(request)
    total = str(cart.get_total_sum())
    total.replace('.', '')
    total = int(float(total))
    stripe.api_key = 'sk_test_51JEYdQGDKcoJktMzd3Gu6X8gKtDwg2JSOo9cf59g0ZbcM39JKGisIseNSIUtoRCun8jlm5A4Kaely884kfMhOfvd00mRpeOQ7k '
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/order_placed.html')
