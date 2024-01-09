
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction, TaxSummary, CurrencyRate, TaxCalculation
import re
from django.conf import settings
from transactions.logic import save_data_from_file, calculate_tax_to_pay


@receiver(post_save, sender=ImportFile)
def save_data_from_file_signal(sender, instance, *args, **kwargs):
    save_data_from_file(instance)


@receiver(post_save, sender=Transaction)
def calculate_tax_to_pay_signal(sender, instance, *args, **kwargs):
    calculate_tax_to_pay(instance)
    # tax_year = instance.executed_at.year
    # if instance.asset_type == "Equity and Index Options":
    #     transaction_currency = instance.currency.lower()
    #     transaction_date = instance.executed_at.date()
    #     print(instance.executed_at.date())
    #     # NOTE move it to reusable funtion? in utils file
    #     previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=transaction_date).order_by('-date').first()
    #     print(previous_day_currency_rate)

    #     option_premium_pln = round(instance.value * getattr(previous_day_currency_rate, transaction_currency), 2)
    #     tax_to_pay_from_transaction = round(option_premium_pln * settings.TAX_RATE, 2)

    #     print(tax_year)
    #     # NOTE different funtion for options: https://github.com/AdamMisiak/Tax_assistant/blob/master/options.py#L49
    #     # update_tax_object(tax_year, tax_to_pay_from_transaction)

    # elif instance.asset_type == "Stocks" and instance.side == "Sell":
    #     closing_transaction = instance
    #     print(closing_transaction)
    #     matching_transactions = Transaction.objects.filter(asset_name=closing_transaction.asset_name, side="Buy").order_by("executed_at")
    #     print(matching_transactions)
    #     if len(matching_transactions) == 1:
    #         opening_transaction = matching_transactions[0]
    #         # NOTE make quantity abs when saving transactions? instead of here everytime?
    #         if opening_transaction.quantity == abs(closing_transaction.quantity):
    #             print(opening_transaction)
    #             profit_or_loss = round(closing_transaction.value_pln + opening_transaction.value_pln, 2)
    #             tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)
    #             print(opening_transaction.value_pln)
    #             print(closing_transaction.value_pln)
    #             print(profit_or_loss)
    #             print(tax_to_pay_from_transaction)
    #             TaxCalculation.objects.create(
    #                 opening_transaction=opening_transaction,
    #                 closing_transaction=closing_transaction,
    #                 revenue=closing_transaction.value_pln,
    #                 cost=opening_transaction.value_pln,
    #                 profit_or_loss=profit_or_loss,
    #                 tax=tax_to_pay_from_transaction
    #             )
    #             update_tax_object(tax_year, closing_transaction.value_pln, opening_transaction.value_pln, tax_to_pay_from_transaction)

    #     elif len(matching_transactions) > 1:
    #         pass


