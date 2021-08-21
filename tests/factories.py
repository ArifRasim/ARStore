import factory
from factory.django import DjangoModelFactory
from faker import Faker

from ARStore.apps.accounts.models import Customer, Address
from ARStore.apps.cart.cart import Cart
from ARStore.apps.checkout.models import DeliveryOptions, PaymentSelections
from ARStore.apps.orders.models import Order, OrderItem
from ARStore.apps.store.models import Category, ProductType, Product, ProductSpecification, ProductSpecificationValue

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'django'
    slug = 'django'


class ProductTypeFactory(DjangoModelFactory):
    class Meta:
        model = ProductType

    name = 'book'


class ProductSpecificationFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    name = 'classic'
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = 'WarandPeace'
    category = factory.SubFactory(CategoryFactory)
    slug = 'WarandPeace'
    price = 5
    discount_price = 3


class ProductSpecificationValueFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = 22


class CustomerFactory(DjangoModelFactory):
    class Meta:
        django_get_or_create = ('email',)
        model = Customer

    email = factory.Iterator(["a@a.com", "b@.b.com", "c@c.com"])
    name = 'arif'
    is_active = True
    password = '123123'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if 'is_superuser' in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    full_name = 'Arif Rasim'
    phone = '123'
    postcode = '123'
    address_line_1 = '123'
    address_line_2 = '123'
    city = '123'
    delivery_instructions = '123'


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart


class PaymentSelectionsFactory(DjangoModelFactory):
    class Meta:
        model = PaymentSelections

    name = 'arif'


class DeliveryOptionsFactory(DjangoModelFactory):
    class Meta:
        model = DeliveryOptions

    delivery_name = 'Arif Rasim'
    delivery_price = 123
    delivery_method = '123'
    delivery_timeframe = '123'
    delivery_window = '123'
    order = 1


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(CustomerFactory)
    full_name = 'Arif Rasim'
    address1 = '123'
    address2 = '123'
    city = '123'
    phone = '123'
    postal_code = '123'
    order_key = '123'
    total_paid = 1


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    price = 1
