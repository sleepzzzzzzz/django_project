from django.db import models


def recalc_cart(cart):
    cart_data = cart.products.aggregate( models.Count('id'))


    cart.total_products = cart_data['id__count']
    cart.save()