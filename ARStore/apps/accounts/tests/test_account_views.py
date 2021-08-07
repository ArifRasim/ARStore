from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, Permission
from django.test import Client, TestCase
import pytest
from django.urls import reverse
from ARStore.apps.accounts.forms import UserEditForm
from ARStore.apps.accounts.models import Customer, CustomAccountManager, Address
from ARStore.apps.store.models import Product

UserModel = get_user_model()


# @pytest.mark.django_db
# def test_dashboard_view(client, customer):
#     user = customer
#     client.force_login(user)
#     url = reverse('account:dashboard')
#     response = client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_register_view_is_authenticated(client, customer):
#     user = customer
#     client.force_login(user)
#     url = reverse('account:register_view')
#     response = client.get(url)
#     assert response.status_code == 302


# class TestView(TestCase):
#     def setUp(self):
#         self.register_url = reverse('account:register_view')
#         self.edit_url = reverse('account:edit_view')
#         self.client = Client()
#         self.user = UserModel.objects.create_user(email='z@z.com', name='arif', password='arif123123', )
#
#
# class RegisterTest(TestView):
#     def test_can_view(self):
#         response = self.client.get(self.register_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_register_user(self):
#         response = self.client.post(self.register_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 302)

# def test_register_user_fails(self):
#     self.user['password'] = 'arifrasim123'
#     response = self.client.post(self.register_url, self.user, format='text/html')
#     self.assertEqual(response.status_code, 400)


# @pytest.mark.django_db
# class DetailsView(TestView):
#     def test_can_view(self):
#         client = Client()
#         client.login()
#         response = self.client.get(self.edit_url)
#         self.assertEqual(response.status_code, 302)


# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#
#     def testLogin(self):
#         self.client.login(username='john', password='johnpassword')
#         response = self.client.get(reverse('account:edit_view'))
#         self.assertEqual(response.status_code, 200)

# class EditDetailsTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # self.user = UserModel.objects.create_user(email='z@z.com',name='arif',password='arif123123')
#         # self.user.set_password('arif123123')
#         # self.user.save()
#         # self.response = self.client.login(email='x@x.com',
#         #                                   password='arif123123')
#         User = get_user_model()
#         self.user = User.objects.create_user(email='z@z.com', name='arif', password='arif123123')
#         self.password = 'example password'
#         self.user.set_password(self.password)
#
#     def test_edit_when_logged(self):
#         # login = self.client.login(email='z@z.com',password='arif123123')
#         # self.response= self.client.get(reverse('account:edit_view'))
#         # self.assertEqual(200, self.response.status_code)
#         # self.client.force_login(self.user)
#         # response = self.client.get(reverse('account:edit_view'))
#         # print(response)
#         # self.assertEqual(response.status_code,200)
#         # User = get_user_model()
#         # self.client.login(email='z@z.com', password='arif123123')
#         # response = self.client.get(reverse('account:edit_view'))
#         # print(response)
#         # self.assertEqual(response.status_code, 201)
#         self.client.login(email=self.user.email, password=self.password)
#         self.client.force_authenticate(self.user)
#         token = Token.objects.create(user=self.user)

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
    response = client.post(reverse('account:edit_address', kwargs={'id': address.id}), {'full_name': '', 'phone': '123123',
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
    response = client.post(reverse('account:edit_address', kwargs={'id': address.id}), {'full_name': 'arifrasim', 'phone': '123123',
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


# def test_set_default_address(customer):
#     address = Address.objects.create(full_name='arif', phone='123123',
#                                      address_line_1='address1', address_line_2='address2',
#                                      city='asenovgrad', postcode='123', customer=customer)
#     client = Client()
#     client.force_login(customer)
#     print(address.id)
#     response = client.post(reverse('account:set_default_address', kwargs={'id': address.id}))
#     print(response)
#     assert response.status_code == 302


def test_add_to_wishlist(customer,category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11,category=category)
    client = Client()
    client.force_login(customer)
    print(product.id)
    response = client.post(reverse('account:add_to_wishlist', kwargs={'id': product.id}))
    print(response)
    assert response.status_code == 302


def test_remove_from_wishlist(customer,category):
    product = Product.objects.create(title='arif', description='123123',
                                     slug='arif', price=20,
                                     discount_price=11,category=category)
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

