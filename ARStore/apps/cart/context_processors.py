from ARStore.apps.cart.cart import Cart


def cart(request):
    return {'cart': Cart(request)}