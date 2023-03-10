# Generated by Django 4.1.6 on 2023-02-12 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_discount_tax_item_currency_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('usd', 'USD'), ('rub', 'RUB')], max_length=3),
        ),
    ]
