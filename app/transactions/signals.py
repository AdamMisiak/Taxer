
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction, TaxSummary, CurrencyRate, TaxCalculation
import re
from django.conf import settings
from transactions.logic import save_data_from_file


@receiver(post_save, sender=ImportFile)
def save_transactions_from_the_file(sender, instance, *args, **kwargs):
    save_data_from_file(instance)
    # asset_index = 5
    # asset_type_index = 3
    # price_index = 8
    # quantity_index = 7
    # value_index = 10
    # currency_index = 4
    # fee_index = 11
    # executed_at_index = 6
    # with instance.file.open('r') as file:

    #     # NOTE close those in separated functions in logic file?
    #     # RATES FILE
    #     if instance.file.name.startswith("Rates"):
    #         csvreader = csv.reader(file, delimiter=';')
    #         for row in csvreader:
    #             if len(row) == 0 or not re.match(r"^([\d]+)$", row[0]):
    #                 continue
    #             print(row)

    #             currency_rate, created = CurrencyRate.objects.get_or_create(
    #                 date=datetime.strptime(row[0], '%Y%m%d'),
    #                 defaults = {
    #                     "usd": float(row[2].replace(",", ".")),
    #                     "eur": float(row[8].replace(",", ".")),
    #                     "gbp": float(row[11].replace(",", ".")),
    #                     "rub": float(row[30].replace(",", ".")) if row[30] else None,
    #                 }
    #             )
    #             print(currency_rate)

    #     # BROKER FILE
    #     elif instance.file.name.startswith("IB"):
    #         csvreader = csv.reader(file)
    #         for row in csvreader:
    #             row_type = row[0]

    #             # TRANSACTION
    #             if row_type == "Trades" and row[1] == "Data":
    #                 print(row)
    #                 # if jest numer konta to go usun
    #                 if row[5].startswith("U"):
    #                     del row[5]

    #                 # print("TRADE")
    #                 # TODO make it atomic
    #                 formatted_asset_type = row[asset_type_index].replace(" - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC", "").strip()
    #                 print(formatted_asset_type)
    #                 is_option = formatted_asset_type in ["Equity and Index Options"]
    #                 executed_at = datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
    #                 previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by('-date').first()
    #                 transaction, created = Transaction.objects.get_or_create(
    #                     asset=row[asset_index],
    #                     side="Buy" if float(row[quantity_index].replace(",", "")) > 0 else "Sell",
    #                     # asset_type=row[asset_type_index],
    #                     price=float(row[price_index]),
    #                     quantity=float(row[quantity_index].replace(",", "")),
    #                     # value=float(row[value_index]),
    #                     # currency=row[currency_index],
    #                     # fee=float(row[fee_index]),
    #                     # option_type=get_option_type(row[asset_index]) if is_option else "",
    #                     # strike_price=get_strike_price(row[asset_index]) if is_option else None,
    #                     executed_at=datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6),
    #                     defaults={
    #                         'asset_type': formatted_asset_type,
    #                         'value': float(row[value_index]),
    #                         'value_pln': round(float(row[value_index]) * getattr(previous_day_currency_rate, row[currency_index].lower()), 2) if row[currency_index].lower() != "pln" else float(row[value_index]),
    #                         'currency': row[currency_index],
    #                         'previous_day_currency_rate': previous_day_currency_rate,
    #                         'fee': float(row[fee_index]),
    #                         'option_type': get_option_type(row[asset_index]) if is_option else "",
    #                         'strike_price': get_strike_price(row[asset_index]) if is_option else None,
    #                     }
                    # )

def update_tax_object(tax_year, revenue, cost, tax):
    previous_state, created = TaxSummary.objects.get_or_create(year=tax_year, defaults={
        'revenue': 0,
        'cost': 0,
        'tax': 0
    })
    tax_object, created = TaxSummary.objects.update_or_create(
        year=tax_year,
        defaults={
            'revenue': round(previous_state.revenue+revenue, 2),
            'cost': round(previous_state.cost+cost, 2),
            'tax': round(previous_state.tax+tax, 2)
        }
    )
    print(tax_object.tax)


@receiver(post_save, sender=Transaction)
def calculate_tax_to_pay(sender, instance, *args, **kwargs):
    tax_year = instance.executed_at.year
    if instance.asset_type == "Equity and Index Options":
        transaction_currency = instance.currency.lower()
        transaction_date = instance.executed_at.date()
        print(instance.executed_at.date())
        # NOTE sprawdzic czy to ze nie ma dnia w nbp kursach czy znaczy ze faktycznie bylo swieto
        # NOTE move it to reusable funtion? in utils file
        previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=transaction_date).order_by('-date').first()
        print(previous_day_currency_rate)

        option_premium_pln = round(instance.value * getattr(previous_day_currency_rate, transaction_currency), 2)
        tax_to_pay_from_transaction = round(option_premium_pln * settings.TAX_RATE, 2)

        print(tax_year)
        # NOTE different funtion for options: https://github.com/AdamMisiak/Tax_assistant/blob/master/options.py#L49
        # update_tax_object(tax_year, tax_to_pay_from_transaction)

    elif instance.asset_type == "Stocks" and instance.side == "Sell":
        closing_transaction = instance
        print(closing_transaction)
        matching_transactions = Transaction.objects.filter(asset_name=closing_transaction.asset_name, side="Buy").order_by("executed_at")
        print(matching_transactions)
        if len(matching_transactions) == 1:
            opening_transaction = matching_transactions[0]
            # NOTE make quantity abs when saving transactions? instead of here everytime?
            if opening_transaction.quantity == abs(closing_transaction.quantity):
                print(opening_transaction)
                profit_or_loss = round(closing_transaction.value_pln + opening_transaction.value_pln, 2)
                tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)
                print(opening_transaction.value_pln)
                print(closing_transaction.value_pln)
                print(profit_or_loss)
                print(tax_to_pay_from_transaction)
                TaxCalculation.objects.create(
                    opening_transaction=opening_transaction,
                    closing_transaction=closing_transaction,
                    revenue=closing_transaction.value_pln,
                    cost=opening_transaction.value_pln,
                    profit_or_loss=profit_or_loss,
                    tax=tax_to_pay_from_transaction
                )
                update_tax_object(tax_year, closing_transaction.value_pln, opening_transaction.value_pln, tax_to_pay_from_transaction)

        elif len(matching_transactions) > 1:
            pass


