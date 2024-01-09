

from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction, TaxSummary, CurrencyRate, TaxCalculation
import re
from django.conf import settings

def save_data_from_file(import_file_instance: ImportFile):
    from transactions.logic import save_data_currency_rates_file, save_data_ib_broker_file
    with import_file_instance.file.open('r') as file:
        # RATES FILE
        if import_file_instance.file.name.startswith("Rates"):
            save_data_currency_rates_file(file)

        # BROKER FILE
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
    from transactions.logic import calculate_tax_option, calculate_tax_equity

    # OPTION
    if transaction_instance.asset_type == "Equity and Index Options":
        calculate_tax_option(transaction_instance)

    # STOCK
    elif transaction_instance.asset_type in ["Stocks", "ETFs"] and transaction_instance.side == "Sell":
        calculate_tax_equity(transaction_instance)
        # tax_year = transaction_instance.executed_at.year
        # closing_transaction = instance
        # print(closing_transaction)
        # matching_transactions = Transaction.objects.filter(asset_name=closing_transaction.asset_name, side="Buy").order_by("executed_at")
        # print(matching_transactions)
        # if len(matching_transactions) == 1:
        #     opening_transaction = matching_transactions[0]
        #     # NOTE make quantity abs when saving transactions? instead of here everytime?
        #     if opening_transaction.quantity == abs(closing_transaction.quantity):
        #         print(opening_transaction)
        #         profit_or_loss = round(closing_transaction.value_pln + opening_transaction.value_pln, 2)
        #         tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)
        #         print(opening_transaction.value_pln)
        #         print(closing_transaction.value_pln)
        #         print(profit_or_loss)
        #         print(tax_to_pay_from_transaction)
        #         TaxCalculation.objects.create(
        #             opening_transaction=opening_transaction,
        #             closing_transaction=closing_transaction,
        #             revenue=closing_transaction.value_pln,
        #             cost=opening_transaction.value_pln,
        #             profit_or_loss=profit_or_loss,
        #             tax=tax_to_pay_from_transaction
        #         )
        #         update_tax_object(tax_year, closing_transaction.value_pln, opening_transaction.value_pln, tax_to_pay_from_transaction)

        # elif len(matching_transactions) > 1:
        #     pass
