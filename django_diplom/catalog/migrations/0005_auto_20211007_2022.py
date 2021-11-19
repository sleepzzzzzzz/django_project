# Generated by Django 3.2.7 on 2021-10-07 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_productimage_productspecification_productspecificationvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='value',
        ),
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, help_text='150x150px', null=True, upload_to='images', verbose_name='изображение'),
        ),
    ]