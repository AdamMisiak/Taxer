# Generated by Django 5.0.1 on 2024-01-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CurrencyRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(unique=True)),
                ("usd", models.FloatField()),
                ("eur", models.FloatField()),
                ("gbp", models.FloatField()),
                ("rub", models.FloatField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Currency rate",
                "verbose_name_plural": "Currency rates",
            },
        ),
        migrations.CreateModel(
            name="ImportFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Import file",
                "verbose_name_plural": "Import files",
            },
        ),
        migrations.CreateModel(
            name="Tax",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField(unique=True)),
                ("to_pay", models.FloatField()),
            ],
            options={
                "verbose_name": "Tax",
                "verbose_name_plural": "Taxes",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("asset", models.CharField(max_length=124)),
                (
                    "side",
                    models.CharField(choices=[("Buy", "Buy"), ("Sell", "Sell")], max_length=8),
                ),
                (
                    "asset_type",
                    models.CharField(
                        choices=[
                            ("Stocks", "Stocks"),
                            ("Bonds", "Bonds"),
                            ("Equity and Index Options", "Options"),
                            ("ETFs", "ETFs"),
                        ],
                        max_length=124,
                    ),
                ),
                ("price", models.FloatField()),
                ("quantity", models.FloatField()),
                ("value", models.FloatField()),
                ("value_pln", models.FloatField()),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("USD", "USD"),
                            ("PLN", "PLN"),
                            ("EUR", "EUR"),
                            ("RUB", "RUB"),
                        ],
                        max_length=3,
                    ),
                ),
                ("fee", models.FloatField()),
                (
                    "option_type",
                    models.CharField(
                        blank=True,
                        choices=[("CALL", "CALL"), ("PUT", "PUT")],
                        max_length=4,
                    ),
                ),
                ("strike_price", models.FloatField(blank=True, null=True)),
                ("executed_at", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
                "unique_together": {("asset", "side", "price", "quantity", "executed_at")},
            },
        ),
    ]