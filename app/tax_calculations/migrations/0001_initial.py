# Generated by Django 5.0.1 on 2024-04-22 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0011_alter_assettransaction_asset_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetTaxCalculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.FloatField()),
                ('cost', models.FloatField()),
                ('profit_or_loss', models.FloatField()),
                ('tax_rate', models.FloatField(default=0.19)),
                ('tax', models.FloatField()),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('closing_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_closing_calculation', to='transactions.assettransaction')),
                ('opening_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_opening_calculation', to='transactions.assettransaction')),
            ],
            options={
                'verbose_name': 'Asset tax calculation 🧮',
                'verbose_name_plural': 'Asset tax calculations 🧮',
            },
        ),
    ]
