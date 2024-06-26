# Generated by Django 5.0.1 on 2024-04-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_dividendtransaction_raw_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettransaction',
            name='asset_type',
            field=models.CharField(choices=[('Stocks', 'Stocks'), ('Dividends', 'Dividends'), ('Withholding Tax', 'Withholding Tax')], max_length=124),
        ),
        migrations.AlterField(
            model_name='dividendtransaction',
            name='asset_type',
            field=models.CharField(choices=[('Stocks', 'Stocks'), ('Dividends', 'Dividends'), ('Withholding Tax', 'Withholding Tax')], max_length=124),
        ),
    ]
