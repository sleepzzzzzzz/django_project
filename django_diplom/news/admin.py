from django.contrib import admin
from . import models


class NewsImageAdminInLine(admin.TabularInline):
    model = models.NewsImage
    extra = 0
    max_num = 3





@admin.register(models.New)
class ProductAdmin(admin.ModelAdmin):
    inlines = [NewsImageAdminInLine]


@admin.register(models.Category_news)
class CategoryAdmin(admin.ModelAdmin):
    pass

