import string
import random

from app.database import models
from app.database.models import DiscountType


def generate_code(code_length) -> str:
    code = "".join(random.choices(string.digits, k=code_length))
    return code


def count_cart(cart: models.Cart) -> models.Cart:
    summ = 0
    for cart_item in cart.products:
        summ += cart_item.amount * cart_item.product.price
    if cart.promocode:
        if cart.promocode.type == DiscountType.PERCENT:
            summ *= 1 - cart.promocode.amount
        else:
            summ -= cart.promocode.amount
    cart.total = summ
    return cart
