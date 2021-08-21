import pytest
from pytest_factoryboy import register

from tests.factories import CategoryFactory, ProductTypeFactory, ProductSpecificationFactory, ProductFactory, \
    ProductSpecificationValueFactory, CustomerFactory, AddressFactory, CartFactory, DeliveryOptionsFactory, \
    PaymentSelectionsFactory, OrderFactory, OrderItemFactory

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductFactory)
register(ProductSpecificationValueFactory)
register(CustomerFactory)
register(AddressFactory)
register(CartFactory)
register(DeliveryOptionsFactory)
register(PaymentSelectionsFactory)
register(OrderFactory)
register(OrderItemFactory)


@pytest.fixture
def product_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()
    return product_type


@pytest.fixture
def product_specification(db, product_specification_factory):
    product_specification = product_specification_factory.create()
    return product_specification


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def product_specification_value(db, product_specification_value_factory):
    product_specification_value = product_specification_value_factory.create()
    return product_specification_value


@pytest.fixture
def customer(db, customer_factory):
    customer = customer_factory.create()
    return customer


@pytest.fixture
def admin_user(db, customer_factory):
    customer = customer_factory.create(is_superuser=True, is_staff=True)
    return customer


@pytest.fixture
def address(db, address_factory):
    address = address_factory.create()
    return address


@pytest.fixture
def cart(db, cart_factory):
    cart = cart_factory.create()
    return cart


@pytest.fixture
def delivery_options(db, delivery_options_factory):
    delivery_options = delivery_options_factory.create()
    return delivery_options


@pytest.fixture
def payment_selections(db, payment_selections_factory):
    payment_selections = payment_selections_factory.create()
    return payment_selections


@pytest.fixture
def order(db, order_factory):
    order = order_factory.create()
    return order


@pytest.fixture
def order_item(db, order_item_factory):
    order_item = order_item_factory.create()
    return order_item