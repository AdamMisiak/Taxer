        

from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction, TaxSummary, CurrencyRate, TaxCalculation
import re
from django.conf import settings

def calculate_tax_option(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    transaction_date = transaction_instance.executed_at.date()
    transaction_currency = transaction_instance.currency.lower()
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=transaction_date).order_by('-date').first()

    option_premium_pln = round(transaction_instance.value * getattr(previous_day_currency_rate, transaction_currency), 2)
    tax_to_pay_from_transaction = round(option_premium_pln * settings.TAX_RATE, 2)

    # NOTE different funtion for options: https://github.com/AdamMisiak/Tax_assistant/blob/master/options.py#L49
    # update_tax_object(tax_year, tax_to_pay_from_transaction)


def calculate_tax_equity(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    closing_transaction = transaction_instance

    # NOTE after refactor add a lot of prints here
    matching_transactions = Transaction.objects.filter(asset_name=closing_transaction.asset_name, side="Buy").order_by("executed_at")
    print(matching_transactions)
    if len(matching_transactions) == 1:
        opening_transaction = matching_transactions[0]
        if opening_transaction.quantity == closing_transaction.quantity:
            print(opening_transaction)
            # NOTE separated function here with _
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