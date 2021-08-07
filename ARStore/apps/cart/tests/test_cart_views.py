import pytest
from django.urls import reverse
from django.test import Client

from ARStore.apps.store.models import Product


@pytest.mark.django_db
def test_cart_view():
    client = Client()
    response = client.get(reverse('cart:cart_summary'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_add(category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    response = client.post(reverse('cart:cart_add'), data={'product_id': product.id, 'product_qty': 1})
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_add_action_is_post(category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    response = client.post(reverse('cart:cart_add'), data={'action':'POST','product_id': product.id, 'product_qty': 1})
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_remove(category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    response = client.post(reverse('cart:cart_remove'), data={'product_id': product.id})
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_update(category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    response = client.post(reverse('cart:cart_update'), data={'product_id': product.id,'updated_qty':1})
    assert response.status_code == 200
