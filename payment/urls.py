from django.urls import path

from payment.views import cart_view, order_placed, stripe_webhook

app_name = 'payment'
urlpatterns = [
    path('', cart_view, name='cart'),
    path('orderplaced/', order_placed, name='order_placed'),
    path('webhook/', stripe_webhook)
]
