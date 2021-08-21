from django.test import Client
from django.urls import reverse

from ARStore.apps.accounts.models import Address
from ARStore.apps.checkout.models import DeliveryOptions


def test_checkout_view(customer):
    delivery_option = DeliveryOptions.objects.create(delivery_name='Arif Rasim',
                                                     delivery_price=123,
                                                     delivery_method='123',
                                                     delivery_timeframe='123',
                                                     delivery_window='123',
                                                     order=1)
    client = Client()
    client.force_login(customer)
    response = client.get(reverse('checkout:delivery_options'))
    assert response.status_code == 200


def test_cart_update(customer, ):
    delivery_option = DeliveryOptions.objects.create(delivery_name='Arif Rasim',
                                                     delivery_price=123,
                                                     delivery_method='123',
                                                     delivery_timeframe='123',
                                                     delivery_window='123',
                                                     order=1)
    client = Client()
    client.force_login(customer)
    print(delivery_option.id)
    print(delivery_option)
    response = client.post(reverse('checkout:cart_update_delivery'), data={'delivery_option': delivery_option.id})
    print(response)
    assert response.status_code == 200


def test_delivery_address_view_without_purchase(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('checkout:delivery_address'), )
    print(response)
    assert response.status_code == 302


def test_delivery_address_view_with_purchase_wo_delivery_address(customer):
    client = Client()
    client.force_login(customer)
    session = client.session
    session['purchase'] = 'purchase'
    session.save()
    response = client.post(reverse('checkout:delivery_address'), )
    print(response)
    assert response.status_code == 302


def test_delivery_address_view_with_purchase_with_delivery_address(customer):
    delivery_address = Address.objects.create(full_name='Arif Rasim',
                                              phone='123',
                                              postcode='123',
                                              address_line_1='123',
                                              address_line_2='123',
                                              city='123', delivery_instructions='123', customer=customer)

    delivery_option = DeliveryOptions.objects.create(delivery_name='Arif Rasim',
                                                     delivery_price=123,
                                                     delivery_method='123',
                                                     delivery_timeframe='123',
                                                     delivery_window='123',
                                                     order=1)

    client = Client()
    client.force_login(customer)
    session = client.session
    session['purchase'] = {'delivery_id': delivery_option.id}
    session.save()
    response = client.post(reverse('checkout:delivery_address'), )
    print(response)
    assert response.status_code == 200


def test_delivery_address_view_with_purchase_with_delivery_address_with_address(customer):
    delivery_address = Address.objects.create(full_name='Arif Rasim',
                                              phone='123',
                                              postcode='123',
                                              address_line_1='123',
                                              address_line_2='123',
                                              city='123', delivery_instructions='123', customer=customer)

    delivery_option = DeliveryOptions.objects.create(delivery_name='Arif Rasim',
                                                     delivery_price=123,
                                                     delivery_method='123',
                                                     delivery_timeframe='123',
                                                     delivery_window='123',
                                                     order=1)

    client = Client()
    client.force_login(customer)
    session = client.session
    session['purchase'] = {'delivery_id': delivery_option.id}
    session['address'] = {'address_id': delivery_option.id}
    session.save()
    response = client.post(reverse('checkout:delivery_address'), )
    print(response)
    assert response.status_code == 200


def test_payment_selection_view_without_address(customer):
    client = Client()
    client.force_login(customer)
    response = client.post(reverse('checkout:payment_selection'), )
    print(response)
    assert response.status_code == 302


def test_payment_selection_view_with_address(customer):
    client = Client()
    client.force_login(customer)
    session = client.session
    session['address'] = 'address'
    session.save()
    response = client.post(reverse('checkout:payment_selection'), )
    print(response)
    assert response.status_code == 200


def test_payment_successful(customer):
    client = Client()
    client.force_login(customer)
    session = client.session
    session['address'] = 'address'
    session['purchase'] = 'address'
    session.save()
    response = client.post(reverse('checkout:payment_successful'), )
    print(response)
    assert response.status_code == 200
