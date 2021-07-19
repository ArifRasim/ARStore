from django.contrib import admin

# Register your models here.
from accounts.models import UserBase

admin.site.register(UserBase)