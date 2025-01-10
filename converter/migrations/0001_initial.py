# Generated by Django 5.1.4 on 2025-01-10 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('rate', models.DecimalField(decimal_places=6, max_digits=20)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConversionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('converted_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('conversion_rate', models.DecimalField(decimal_places=6, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_currency', to='converter.currency')),
                ('to_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_currency', to='converter.currency')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=20)),
                ('rate_date', models.DateField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='converter.currency')),
            ],
        ),
    ]
