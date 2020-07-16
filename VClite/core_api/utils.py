def validate_order(order):
    if order.quantity <= 0:
        return False
    else:
        return True
