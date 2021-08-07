from django.urls import path

from ARStore.apps.checkout import views
from ARStore.apps.checkout.views import DeliveryOptionsView

app_name = 'checkout'

urlpatterns = [
    path("delivery_options/", DeliveryOptionsView.as_view(), name="delivery_options"),
    path("cart_update_delivery/", views.cart_update_delivery, name="cart_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]