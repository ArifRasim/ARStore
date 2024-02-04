import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_root_url(client):
    url = reverse('store:all_products')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search():
    client = Client()
    response = client.post(reverse('store:search_products'), data={'q': 'a'})
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_empty():
    client = Client()
    response = client.post(reverse('store:search_products'), data={'q': ''})
    print(response)
    assert response.status_code == 200
