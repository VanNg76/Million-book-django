# Generated by Django 4.0.5 on 2022-06-18 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0006_alter_orderbook_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderbook',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_books', to='app_api.order'),
        ),
    ]
