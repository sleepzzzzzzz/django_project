from collections import defaultdict
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from django.views.generic import TemplateView

from cart.models import CartProduct, CartAddon
from catalog.models import Category, Product, Addon


class HomeTemplateView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            total=Count('product', distinct=True) + Count('addon', distinct=True))

        return context


@login_required
def home(request):
    cat = Category.objects.annotate(Count('product'))
    return render(
        request,
        'catalog/home.html',
        {
            "categories": cat,

        }
    )


class MenTemplate(TemplateView):
    template_name = "catalog/Men.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(total=Count('product', distinct=True)).filter(gender='male')

        return context


def men(request):
    cat = Category.objects.annotate(Count('product'))
    return render(
        request,
        'catalog/Men.html',
        {
            "categories": cat,

        }
    )


def kids(request):
    cat = Category.objects.filter(gender='kids')
    return render(
        request,
        'catalog/Kids.html',
        {
            "categories": cat,

        }
    )


def women(request):
    cat = Category.objects.filter(gender='female')
    return render(
        request,
        'catalog/Women.html',
        {
            "categories": cat,
        }
    )


def accessory(request):
    cat = Category.objects.filter(gender='accessory')
    return render(
        request,
        'catalog/Women.html',
        {
            "categories": cat,
        }
    )


def addon(request):
    addon = Category.objects.annotate(Count('addon'))
    return addon


def cat(request: WSGIRequest, category_slug: str) -> HttpResponse:
    try:

        category: Category = (Category.objects.prefetch_related("product_set").get(slug=category_slug))
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'catalog/home.html', {'category': category})


@login_required
def one_cat(request, category_slug):
    cat = Category.objects.prefetch_related("product_set").prefetch_related("addon_set__product_set").filter(
        slug=category_slug).first()

    return render(
        request,
        'catalog/one_categories.html',
        {"categories": cat,
         "addons": addon(request)
         }

    )


def prod_view(request, product_slug):
    product = Product.objects.prefetch_related("addons").prefetch_related("addons__category").filter(
        slug=product_slug).first()

    mapper = defaultdict(list)

    for a in product.addons.all():
        mapper[a.category.name].append(a)

    return render(
        request,
        'catalog/product.html',
        {
            "products": product,
            "addons_mapper": dict(mapper),
            'is_product_in_cart': is_product_in_cart(product, request.user)

        }
    )


def addon_view(request, addon_slug):
    add = Addon.objects.filter(slug=addon_slug).first()

    return render(
        request,
        'catalog/addon.html',
        {
            "addon": add,
            'is_addon_in_cart': is_addon_in_cart(add, request.user)

        }
    )


def is_product_in_cart(product, user):
    is_exists = CartProduct.objects.filter(product=product, cart__user=user,
                                           cart__checked_out=False).exists()
    return is_exists


def is_addon_in_cart(addon, user):
    is_addon_exists = CartAddon.objects.filter(addon=addon, cart__user=user,
                                               cart__checked_out=False).exists()
    return is_addon_exists
