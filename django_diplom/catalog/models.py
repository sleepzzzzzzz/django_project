from colorfield.fields import ColorField
from django.db import models

gender = (
    ('male', 'male'),
    ('female', 'female'),
    ('kids', 'kids'),
    ('accessory', 'accessory'),
)

COLOR_CHOICES = [
    ("#FFFFFF", "white"),
    ("#000000", "black")

]


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='описание')
    slug = models.SlugField(max_length=40, unique=True)
    gender = models.CharField(default='', max_length=9, choices=gender, verbose_name="gender")

    def __str__(self):
        return self.name


class Addon(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена')
    slug = models.SlugField(max_length=40, unique=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class AddonImage(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images', help_text='150x150px',
                              verbose_name='изображение')
    addon = models.ForeignKey('Addon', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена')
    slug = models.SlugField(max_length=40, unique=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    addons = models.ManyToManyField("Addon", blank=True)
    quantity = models.PositiveIntegerField(default=1)




    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images', help_text='150x150px',
                              verbose_name='изображение')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class ProductSpecification(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование характеристики')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    specification = models.ForeignKey('ProductSpecification', on_delete=models.CASCADE)
    value = models.CharField(max_length=128, verbose_name='Значение характеристики')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'

    def __str__(self):
        return f'{self.specification.name} - {self.value}'


class AddonSpecification(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование характеристики')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class AddonSpecificationValue(models.Model):
    specification = models.ForeignKey('AddonSpecification', on_delete=models.CASCADE)
    value = models.CharField(max_length=128, verbose_name='Значение характеристики')
    product = models.ForeignKey('Addon', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'

    def __str__(self):
        return f'{self.specification.name} - {self.value}'
