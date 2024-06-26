# Generated by Django 5.0.1 on 2024-06-16 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_calculations', '0002_dividendtaxcalculation'),
        ('transactions', '0015_alter_assettransaction_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionTaxCalculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.FloatField()),
                ('cost', models.FloatField()),
                ('profit_or_loss', models.FloatField()),
                ('tax_rate', models.FloatField(default=0.19)),
                ('tax', models.FloatField()),
                ('closing_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_closing_calculation', to='transactions.optiontransaction')),
                ('opening_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_opening_calculation', to='transactions.optiontransaction')),
            ],
            options={
                'verbose_name': 'Option tax calculation 🧮',
                'verbose_name_plural': 'Option tax calculations 🧮',
            },
        ),
    ]
