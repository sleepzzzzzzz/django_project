# Generated by Django 3.2.7 on 2021-10-22 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Category_new',
        ),
        migrations.RenameModel(
            old_name='News',
            new_name='New',
        ),
    ]
