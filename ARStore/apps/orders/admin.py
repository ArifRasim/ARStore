from django.contrib import admin

# Register your models here.
from ARStore.apps.orders.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)