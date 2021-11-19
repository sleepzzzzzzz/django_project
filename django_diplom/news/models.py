from django.db import models


class New(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='описание')
    slug = models.SlugField(max_length=40, unique=True)
    category = models.ForeignKey("Category_news", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Category_news(models.Model):
    name = models.CharField(max_length=32, verbose_name='Наименование')
    description = models.TextField(max_length=256, verbose_name='описание')
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class NewsImage(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images', help_text='450x450px',
                              verbose_name='изображение')
    new = models.ForeignKey('New', on_delete=models.CASCADE)
