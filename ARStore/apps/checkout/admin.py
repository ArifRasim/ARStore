from django.contrib import admin

# Register your models here.
from ARStore.apps.checkout.models import DeliveryOptions

admin.site.register(DeliveryOptions)