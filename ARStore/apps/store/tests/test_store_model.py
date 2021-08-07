from django.urls import reverse


def test_category_str(product_category):
    assert product_category.__str__() == 'django'


def test_category_get_absolute_url(client, product_category):
    category = product_category
    category.get_absolute_url()
    url = reverse('store:category_list', args=[category.slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_type_str(product_type):
    assert product_type.__str__() == 'book'


def test_product_specification_str(product_specification):
    assert product_specification.__str__() == 'classic'


def test_product_str(product):
    assert product.__str__() == 'WarandPeace'


def test_product_get_absolute_url(client, product):
    product= product
    product.get_absolute_url()
    url = reverse('store:product_detail', args=[product.slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_specification_value(product_specification_value):
    assert product_specification_value.__str__() == 22
