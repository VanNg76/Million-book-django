# Generated by Django 4.0.4 on 2022-06-08 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0004_rename_bookcategories_bookcategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookCategory',
        ),
    ]
