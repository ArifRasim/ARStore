from decimal import Decimal

from ARStore import settings
from ARStore.apps.checkout.models import DeliveryOptions
from ARStore.apps.store.models import Product


class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty

        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': qty}
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def update(self, product, updated_qty):
        product_id = str(product.id)
        # updated_qty = str(updated_qty)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = updated_qty
        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.session['address']
        del self.session['purchase']
        self.save()

    def cart_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def get_delivery_price(self):
        new_price = 0.00

        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return new_price

    def get_total_price(self):
        new_price = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(new_price)
        return total
