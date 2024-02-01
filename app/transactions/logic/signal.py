import csv
import re
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import CurrencyRate, ImportFile, TaxCalculation, TaxSummary, Transaction, Dividend

def _get_tax_year_from_file(file_name: str) -> float:
    regex_pattern = re.compile(r'(?<!\d)\d{4}(?!\d)')
    match = re.search(regex_pattern, file_name)
    if match:
        return float(match.group())
    else:
        raise Exception(f"🛑 Failed to find tax year in '{file_name}'.")

def save_data_from_file(import_file_instance: ImportFile):
    from transactions.logic import init_tax_summary, save_data_currency_rates_file, save_data_dif_broker_file, save_data_ib_broker_file

    with import_file_instance.file.open("r") as file:
        tax_year = _get_tax_year_from_file(str(import_file_instance.file))
        
        # TaxSummary init
        init_tax_summary(tax_year)

        # RATES FILE
        if import_file_instance.file.name.startswith("Rates"):
            save_data_currency_rates_file(file)

        # IB BROKER FILE
        elif import_file_instance.file.name.startswith("IB"):
            save_data_ib_broker_file(file)

        # DIF BROKER FILE
        elif import_file_instance.file.name.startswith("DIF"):
            save_data_dif_broker_file(file)

        # NOTE hadnle XTB fie? or handled by broker 


def calculate_tax_to_pay(model_instance: Transaction | Dividend):
    from transactions.logic import calculate_tax_dividend, calculate_tax_equity, calculate_tax_option

    # OPTION
    if isinstance(model_instance, Transaction) and model_instance.asset_type == "Equity and Index Options":
        calculate_tax_option(model_instance)

    # STOCK
    elif isinstance(model_instance, Transaction) and model_instance.asset_type in ["Stocks", "ETFs"] and model_instance.side == "Sell":
        calculate_tax_equity(model_instance)

    # DIVIDEND
    # TODO check if how much tax was paid
    elif isinstance(model_instance, Dividend):
        calculate_tax_dividend(model_instance)


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
