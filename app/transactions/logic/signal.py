import csv
import re
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import CurrencyRate, ImportFile, TaxCalculation, TaxSummary, Transaction


def save_data_from_file(import_file_instance: ImportFile):
    from transactions.logic import save_data_currency_rates_file, save_data_ib_broker_file

    with import_file_instance.file.open("r") as file:
        # RATES FILE
        if import_file_instance.file.name.startswith("Rates"):
            save_data_currency_rates_file(file)

        # IB BROKER FILE
        elif import_file_instance.file.name.startswith("IB"):
            save_data_ib_broker_file(file)


# def update_tax_object(tax_year, revenue, cost, tax):
#     previous_state, created = TaxSummary.objects.get_or_create(year=tax_year, defaults={
#         'revenue': 0,
#         'cost': 0,
#         'tax': 0
#     })
#     tax_object, created = TaxSummary.objects.update_or_create(
#         year=tax_year,
#         defaults={
#             'revenue': round(previous_state.revenue+revenue, 2),
#             'cost': round(previous_state.cost+cost, 2),
#             'tax': round(previous_state.tax+tax, 2)
#         }
#     )
#     print(tax_object.tax)


def calculate_tax_to_pay(transaction_instance: Transaction):
    from transactions.logic import calculate_tax_dividend, calculate_tax_equity, calculate_tax_option

    # OPTION
    if transaction_instance.asset_type == "Equity and Index Options":
        calculate_tax_option(transaction_instance)

    # STOCK
    elif transaction_instance.asset_type in ["Stocks", "ETFs"] and transaction_instance.side == "Sell":
        calculate_tax_equity(transaction_instance)

    # calculate_tax_dividend
