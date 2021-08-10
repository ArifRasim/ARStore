def test_order_str(order):
    order.__str__()
    assert     order.__str__() != 'now'



def test_order_item_str(order_item):
    order_item.__str__()
    assert order_item.__str__() == str(order_item.product)