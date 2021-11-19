from django.db import models
from django.utils import timezone

from django_diplom import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64, verbose_name=' Полное имя')
    phone_number = models.CharField(max_length=16, verbose_name='номер телефона')
    email = models.EmailField(max_length=32, verbose_name='email')
    orders = models.ManyToManyField('Order', verbose_name='Заказы', related_name='related_customer')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.Model)
    date_created = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class CartProduct(models.Model):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def product_price(self):
        full_price = self.product.price * self.product.quantity
        return full_price


class CartAddon(models.Model):
    addon = models.ForeignKey('catalog.Addon', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def addon_price(self):
        full_price_addon = self.addon.price * self.addon.quantity
        return full_price_addon


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'новый заказ'),
        (STATUS_IN_PROGRESS, 'закакз в обработке'),
        (STATUS_READY, 'заказ готов'),
        (STATUS_COMPLETED, 'заказ выполнен')

    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'самовывоз'),
        (BUYING_TYPE_DELIVERY, 'доставка')
    )
    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE,
                                 related_name='related_orders')

    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    cart = models.ForeignKey('Cart', verbose_name='корзина', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name='email',null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name='адресс', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='статус заказа ', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=100,
        verbose_name="тип заказа",
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF)
    comment = models.TextField(verbose_name='комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='время создания заказа')
    order_date = models.DateTimeField(verbose_name='дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
