# Generated by Django 4.1.5 on 2023-03-09 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_order_price_element_price_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_from',
            field=models.TimeField(blank=True, null=True, verbose_name='Дата заказа от'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_to',
            field=models.TimeField(blank=True, null=True, verbose_name='Дата заказа до'),
        ),
    ]
