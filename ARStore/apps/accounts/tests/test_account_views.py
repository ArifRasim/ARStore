from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from ARStore.apps.accounts.models import Address
from ARStore.apps.store.models import Product

UserModel = get_user_model()


def test_edit_view_get(customer):
    client = Client()
    client.force_login(customer)
    response = client.get(reverse('account:edit_view'))
    print(response)
    assert response.status_code == 200


def test_edit_view_post_error(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:edit_view'), {'password': 'arifrasim123123'})
    print(response)
    assert response.status_code == 400


def test_edit_view_post_works(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:edit_view'), {'email': 'a@aaa.com', 'name': 'arifrasim123123'})
    print(response)
    assert response.status_code == 200


def test_delete_account(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:delete_user'))
    print(response)
    assert response.status_code == 302


def test_addresses_view(customer):
    client = Client()
    client.force_login(customer)
    response = client.get(reverse('account:addresses'))
    print(response)
    assert response.status_code == 200


def test_add_addresses_view_get(customer):
    client = Client()
    client.force_login(customer)
    response = client.get(reverse('account:add_address'))
    print(response)
    assert response.status_code == 200


def test_add_addresses_view_post(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:add_address'), {'full_name': 'arifrasim123123', 'phone': '123123',
                                                            'address_line_1': 'address1', 'address_line_2': 'address2',
                                                            'city': 'asenovgrad', 'postcode': '123'})
    print(response)
    assert response.status_code == 302


def test_add_addresses_view_post_invalid_form(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:add_address'), {'full_name': '', 'phone': '123123',
                                                            'address_line_1': 'address1', 'address_line_2': 'address2',
                                                            'city': 'asenovgrad', 'postcode': '123'})
    print(response)
    assert response.status_code == 400


def test_edit_addresses_view(customer):
    address = Address.objects.create(full_name='arif', phone='123123',
                                     address_line_1='address1', address_line_2='address2',
                                     city='asenovgrad', postcode='123', customer=customer)
    client = Client()
    client.force_login(customer)
    print(address.id)
    response = client.get(reverse('account:edit_address', kwargs={'id': address.id}))
    print(response)
    assert response.status_code == 200


def test_edit_addresses_view_post_invalid_form(customer):
    address = Address.objects.create(full_name='arif', phone='123123',
                                     address_line_1='address1', address_line_2='address2',
                                     city='asenovgrad', postcode='123', customer=customer)
    client = Client()
    client.force_login(customer)
    print(address.id)
    response = client.post(reverse('account:edit_address', kwargs={'id': address.id}),
                           {'full_name': '', 'phone': '123123',
                            'address_line_1': 'address1', 'address_line_2': 'address2',
                            'city': 'asenovgrad', 'postcode': '123'})
    print(response)
    assert response.status_code == 400


def test_edit_addresses_view_post_valid_form(customer):
    address = Address.objects.create(full_name='arif', phone='123123',
                                     address_line_1='address1', address_line_2='address2',
                                     city='asenovgrad', postcode='123', customer=customer)
    client = Client()
    client.force_login(customer)
    print(address.id)
    response = client.post(reverse('account:edit_address', kwargs={'id': address.id}),
                           {'full_name': 'arifrasim', 'phone': '123123',
                            'address_line_1': 'address1', 'address_line_2': 'address2',
                            'city': 'asenovgrad', 'postcode': '123'})
    print(response)
    assert response.status_code == 302


def test_edit_delete_address(customer):
    address = Address.objects.create(full_name='arif', phone='123123',
                                     address_line_1='address1', address_line_2='address2',
                                     city='asenovgrad', postcode='123', customer=customer)
    client = Client()
    client.force_login(customer)
    print(address.id)
    response = client.post(reverse('account:delete_address', kwargs={'id': address.id}))
    print(response)
    assert response.status_code == 302


def test_add_to_wishlist(customer, category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    client.force_login(customer)
    print(product.id)
    response = client.post(reverse('account:add_to_wishlist', kwargs={'id': product.id}))
    print(response)
    assert response.status_code == 302


def test_remove_from_wishlist(customer, category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11, category=category)
    client = Client()
    client.force_login(customer)
    print(product.id)
    response = client.post(reverse('account:add_to_wishlist', kwargs={'id': product.id}))
    response = client.post(reverse('account:add_to_wishlist', kwargs={'id': product.id}))
    assert response.status_code == 302


def test_wishlist_view(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:wishlist'))
    assert response.status_code == 200


def test_orders_view(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('account:user_orders'))
    assert response.status_code == 200
