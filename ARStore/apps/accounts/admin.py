from django.contrib import admin

# Register your models here.
from ARStore.apps.accounts.models import Customer, Address

admin.site.register(Customer)
admin.site.register(Address)
