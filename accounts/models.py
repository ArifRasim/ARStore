from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy
from django_countries.fields import CountryField


# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') == False:
            raise ValueError('superuser must be a staff member')

        if other_fields.get('is_active') == False:
            raise ValueError('superuser must be an active member')

        if other_fields.get('is_superuser') == False:
            raise ValueError('superuser must be a superuser')
        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('Email must be provided'))
        email=self.normalize_email(email)
        user=self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user
class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email address'),unique=True)
    username = models.CharField(unique=True, max_length=140)
    first_name = models.CharField(blank=True, max_length=140)
    about = models.TextField(blank=True, max_length=500)
    country = CountryField()
    address_line_1 = models.CharField(blank=True, max_length=140)
    address_line_2 = models.CharField(blank=True, max_length=140)
    city = models.CharField(blank=True, max_length=140)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username
