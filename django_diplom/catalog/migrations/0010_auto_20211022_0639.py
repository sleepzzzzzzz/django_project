# Generated by Django 3.2.7 on 2021-10-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20211021_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='gender',
            field=models.CharField(choices=[('x', 'male'), ('y', 'female'), ('z', 'kids')], default='', max_length=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('x', 'male'), ('y', 'female'), ('z', 'kids')], default='', max_length=1, verbose_name='gender'),
        ),
    ]