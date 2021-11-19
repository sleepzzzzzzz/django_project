# Generated by Django 3.2.7 on 2021-11-09 20:03

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#FFFFFF', 'white'), ('#000000', 'black')], default='#FFFFFF', max_length=18),
        ),
    ]
