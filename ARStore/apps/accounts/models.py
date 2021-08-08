import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get('is_staff'):
            raise ValueError('superuser must be a staff member')

        if not other_fields.get('is_active'):
            raise ValueError('superuser must be an active member')

        if not other_fields.get('is_superuser'):
            raise ValueError('superuser must be a superuser')
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('Email must be provided'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=140)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), on_delete=models.CASCADE)
    full_name = models.CharField(_('Full Name'), max_length=150)
    phone = models.CharField(_('Phone'), max_length=150)
    postcode = models.CharField(_('Post code'), max_length=150)
    address_line_1 = models.CharField(_('Address_line_1'), max_length=250)
    address_line_2 = models.CharField(_('Address_line_2'), max_length=250,blank=True)
    city = models.CharField(_('City'), max_length=150)
    delivery_instructions = models.CharField(_('Delivery instructions'), max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(_('Default'), default=False, )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.full_name
