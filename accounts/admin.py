from django.contrib import admin

# Register your models here.
from accounts.models import Customer, Address

admin.site.register(Customer)
admin.site.register(Address)