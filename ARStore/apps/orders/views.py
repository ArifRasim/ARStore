from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
from ARStore.apps.cart.cart import Cart
from ARStore.apps.orders.models import Order, OrderItem


# @login_required
# def add_order(request):
#     cart = Cart(request)
#     user_id = request.user.id
#     order_key = request.POST.get('order_key')
#     cart_total = cart.get_total_price()
#     if Order.objects.filter(order_key=order_key).exists():
#         pass
#     else:
#         order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
#                                      address2='add2', total_paid=cart_total, order_key=order_key)
#         order_id = order.pk
#         for item in cart:
#             OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
#                                      quantity=item['qty'])
#     response = JsonResponse({'success': 'Return something'})
#     return response


# @login_required
# def payment_confirmation(data):
#     Order.objects.filter(order_key=data).update(billing_status=True)


# @login_required
# def user_orders(request):
#     user_id = request.user.id
#     orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
#
#     return orders
