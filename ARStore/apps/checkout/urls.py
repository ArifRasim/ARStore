from django.urls import path

from ARStore.apps.checkout import views

app_name = 'checkout'

urlpatterns = [
    path("delivery_options/", views.delivery_options, name="delivery_options"),
    path("cart_update_delivery/", views.cart_update_delivery, name="cart_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]