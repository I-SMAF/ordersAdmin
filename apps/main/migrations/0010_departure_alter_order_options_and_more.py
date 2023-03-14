# Generated by Django 4.1.5 on 2023-03-14 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_checkingorder_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_cost', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Стоимость по накладной')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата выезда')),
                ('direction', models.CharField(blank=True, max_length=256, null=True, verbose_name='Направление выезда')),
            ],
            options={
                'verbose_name': 'Отправлено (Выезд)',
                'verbose_name_plural': 'Отправлено (Выезды)',
                'ordering': ['date'],
            },
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='sentorder',
            options={'verbose_name': 'Заказ отправлено', 'verbose_name_plural': 'Отправлено (Заказы)'},
        ),
        migrations.AlterField(
            model_name='order',
            name='date_from',
            field=models.TimeField(blank=True, null=True, verbose_name='Время заказа от'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_to',
            field=models.TimeField(blank=True, null=True, verbose_name='Время заказа до'),
        ),
        migrations.AddField(
            model_name='order',
            name='departure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.departure', verbose_name='Выезд'),
        ),
    ]