from django.contrib import admin
from . import models


class ProductImageAdminInLine(admin.TabularInline):
    model = models.ProductImage
    extra = 0
    max_num = 3


class ProductSpecificationValueInLine(admin.TabularInline):
    model = models.ProductSpecificationValue
    extra = 0
    max_num = 10

class AddonImageAdminInLine(admin.TabularInline):
    model = models.AddonImage
    extra = 0
    max_num = 3


class AddonSpecificationValueInLine(admin.TabularInline):
    model = models.AddonSpecificationValue
    extra = 0
    max_num = 10

@admin.register(models.ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    pass

@admin.register(models.AddonSpecification)
class AddonSpecificationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdminInLine, ProductSpecificationValueInLine]



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Addon)
class AddonAdmin(admin.ModelAdmin):
    inlines = [AddonImageAdminInLine, AddonSpecificationValueInLine]

# Register your models here.
