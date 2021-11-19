from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from cart.models import Cart, CartProduct, CartAddon

User = get_user_model()


def cart_quantity(request):
    if not request.user.is_authenticated:
        context = {
            'None': None}
        return context

    user_cart = Cart.objects.filter(user=request.user, checked_out=False).first()

    cart_product = CartProduct.objects.filter(cart=user_cart).count()
    cart_addon = CartAddon.objects.filter(cart=user_cart).count()
    total_quantity = cart_addon + cart_product

    context = {
        'total_quantity': total_quantity}
    return context
