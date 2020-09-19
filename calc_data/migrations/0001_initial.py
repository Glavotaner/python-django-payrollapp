# Generated by Django 3.1 on 2020-09-19 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionsModality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modality_mark', models.CharField(max_length=4, unique=True, verbose_name='Modality mark')),
                ('pension_fund_one', models.FloatField(default=0.15, verbose_name='Pension fund 1')),
                ('pension_fund_two', models.FloatField(default=0.05, verbose_name='Pension fund 2')),
                ('health_fund', models.FloatField(default=0.165, verbose_name='Health fund')),
            ],
        ),
        migrations.CreateModel(
            name='HourFund',
            fields=[
                ('period_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Period ID')),
                ('month', models.IntegerField(verbose_name='Month')),
                ('total_hours', models.IntegerField(verbose_name='Total hours')),
            ],
        ),
        migrations.CreateModel(
            name='TaxModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lo_tax_bracket', models.FloatField(verbose_name='Low tax bracket')),
                ('hi_tax_bracket', models.FloatField(verbose_name='High tax bracket')),
                ('lo_tax_rate', models.FloatField(verbose_name='Low tax rate')),
                ('hi_tax_rate', models.FloatField(verbose_name='High tax rate')),
                ('valid_from', models.DateField(verbose_name='Valid from')),
            ],
        ),
    ]
