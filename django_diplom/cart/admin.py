from django.contrib import admin
from . import models



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    pass