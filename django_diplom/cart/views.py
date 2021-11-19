from typing import Optional, Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Product, Addon, Category
from cart.models import CartProduct, CartAddon, Customer, Cart
from django_diplom.settings import EMAIL_HOST_USER

from .forms import OrderForm

# add_to_cart/hamurger/?is_addon=0
from .mixins import CartMixin
from .utils import recalc_cart


def add_to_cart(request, product_slug):
    slug_product = Product.objects.get(slug=product_slug)

    new_cart, is_new_cart = Cart.objects.get_or_create(user=request.user, checked_out=False)
    new_product, _ = CartProduct.objects.get_or_create(product=slug_product, cart=new_cart)

    return redirect(reverse('catalog:home'))


def add_to_cart_addon(request, addon_slug):
    slug_addon = Addon.objects.get(slug=addon_slug)

    new_cart, is_new_cart = Cart.objects.get_or_create(user=request.user, checked_out=False)
    new_addon, _ = CartAddon.objects.get_or_create(addon=slug_addon, cart=new_cart)

    return redirect(reverse('catalog:home'))


def cart(request):
    if not request.user.is_authenticated:
        return redirect(reverse('catalog:home'))

    user_cart = Cart.objects.filter(user=request.user, checked_out=False).first()
    if not user_cart:
        user_cart = Cart.objects.create(user=request.user)

    cart_product = CartProduct.objects.filter(cart=user_cart)
    cart_addon = CartAddon.objects.filter(cart=user_cart)

    is_checked_out = False

    context = {
        'total': cart_price(request),
        'cart_product': cart_product,
        'cart_addon': cart_addon,

    }
    return render(request, 'cart/cart.html', context)


def remove_product(request, product_slug):
    slug_product = Product.objects.get(slug=product_slug)
    old_cart = Cart.objects.filter(user=request.user, checked_out=False).first()
    product = CartProduct.objects.get(product=slug_product, cart=old_cart)
    product.delete()

    return redirect(reverse('cart:cart'))


def remove_addon(request, addon_slug):
    slug_addon = Addon.objects.get(slug=addon_slug)
    old_cart = Cart.objects.filter(user=request.user, checked_out=False).first()
    addon = CartAddon.objects.get(addon=slug_addon, cart=old_cart)
    addon.delete()

    return redirect(reverse('cart:cart'))


def parse_int(value: int, default: Optional[Any] = None) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def change_quantity(request, product_slug):
    if request.method == 'POST':

        full_quantity = parse_int(request.POST.get('quantity'))
        product = Product.objects.get(slug=product_slug)
        if full_quantity:
            product.quantity = int(full_quantity)
            changed = False
            product.save()
    return redirect(reverse('cart:cart'))


def change_quantity_addon(request, addon_slug):
    if request.method == 'POST':

        full_quantity = parse_int(request.POST.get('quantity'))
        addon = Addon.objects.get(slug=addon_slug)
        if full_quantity:
            addon.quantity = int(full_quantity)
            addon.save()
    return redirect(reverse('cart:cart'))


def cart_price(request):
    cart = Cart.objects.filter(user=request.user, checked_out=False).prefetch_related("cartproduct_set").first()
    total = 0

    for product in cart.cartproduct_set.all():
        total += product.product_price()
    for addon in cart.cartaddon_set.all():
        total += addon.addon_price()

    return total


# def cart_quantity(request):
#     user_cart = Cart.objects.filter(user=request.user, checked_out=False).first()
#
#     cart_product = CartProduct.objects.filter(cart=user_cart).count()
#     cart_addon = CartAddon.objects.filter(cart=user_cart).count()
#     total_quantity = cart_addon + cart_product
#
#     return total_quantity


def checkout(request):
    user = request.user
    user_cart = Cart.objects.filter(user=request.user, checked_out=False).first()
    cart_product = CartProduct.objects.filter(cart=user_cart)
    cart_addon = CartAddon.objects.filter(cart=user_cart)
    form = OrderForm(request.POST or None)

    is_checked_out = False

    if not user_cart:
        return redirect(reverse('catalog:home'))
    context = {
        'cart_product': cart_product,
        'cart_addon': cart_addon,
        'total': cart_price(request),
        'form': form

    }
    return render(request, 'cart/checkout.html', context)


def MakeOrder(request):
    cart = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.email = form.cleaned_data['email']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            new_order.cart = cart

            subject = 'привет'
            message = 'php это круто '
            recepient = new_order.email
            send_mail(subject,
                      message, EMAIL_HOST_USER, [recepient], fail_silently=False)

            messages.add_message(request, messages.INFO, ' Спасибо за заказ ,менеджер с вами свяжется !')
            new_order.save()
            customer.orders.add(new_order)
            cart.checked_out = True
            cart.save()

            return redirect(reverse('catalog:home'))
        return redirect((reverse('cart:checkout')))


'''class HomeTemplateView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['Cart'] = Cart.objects.annotate(
            products_in_cart=Count('cartproduct', distinct=True) + Count('cartaddon', distinct=True))

        return context'''
