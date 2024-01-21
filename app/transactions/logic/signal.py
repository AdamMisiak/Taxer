import csv
import re
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import CurrencyRate, ImportFile, TaxCalculation, TaxSummary, Transaction


def save_data_from_file(import_file_instance: ImportFile):
    from transactions.logic import init_tax_summary, save_data_currency_rates_file, save_data_ib_broker_file

    with import_file_instance.file.open("r") as file:
        # TaxSummary init
        tax_year = int(str(import_file_instance.file).split("_")[1])
        init_tax_summary(tax_year)

        # RATES FILE
        if import_file_instance.file.name.startswith("Rates"):
            save_data_currency_rates_file(file)

        # IB BROKER FILE
        elif import_file_instance.file.name.startswith("IB"):
            save_data_ib_broker_file(file)

        # NOTE Add DIF broker files for divs + transasctions
        # NOTE hadnle XTB fie? or handled by broker 


def calculate_tax_to_pay(transaction_instance: Transaction):
    from transactions.logic import calculate_tax_dividend, calculate_tax_equity, calculate_tax_option

    # OPTION
    if transaction_instance.asset_type == "Equity and Index Options":
        calculate_tax_option(transaction_instance)

    # STOCK
    elif transaction_instance.asset_type in ["Stocks", "ETFs"] and transaction_instance.side == "Sell":
        calculate_tax_equity(transaction_instance)

    # DIVIDEND
    # calculate_tax_dividend


def update_tax_summary_for_year(tax_calculation_instance: TaxCalculation):
    from transactions.logic import update_tax_summary

    if tax_calculation_instance.closing_transaction:
        tax_year = tax_calculation_instance.closing_transaction.executed_at.year
    elif tax_calculation_instance.opening_transaction:
        tax_year = tax_calculation_instance.opening_transaction.executed_at.year

    update_tax_summary(
        tax_year=tax_year,
        revenue=tax_calculation_instance.revenue,
        cost=tax_calculation_instance.cost,
        tax=tax_calculation_instance.tax,
    )
