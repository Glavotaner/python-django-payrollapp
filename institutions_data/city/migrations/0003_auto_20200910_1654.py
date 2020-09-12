# Generated by Django 3.1 on 2020-09-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0002_city_tax_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='tax_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, verbose_name='Tax amount'),
        ),
    ]
