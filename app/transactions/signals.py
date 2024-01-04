
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction, Tax, CurrencyRate
import re


def get_option_type(option_name: str) -> str:
    return "CALL" if option_name[-1] == "C" else "PUT"

def get_strike_price(option_name: str) -> float:
    return float(option_name.split()[-2])

@receiver(post_save, sender=ImportFile)
def save_transactions_from_the_file(sender, instance, *args, **kwargs):
    asset_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6
    with instance.file.open('r') as file:

        # RATES FILE
        if instance.file.name.startswith("Rates"):
            csvreader = csv.reader(file, delimiter=';')
            for row in csvreader:
                if len(row) == 0 or not re.match(r"^([\d]+)$", row[0]):
                    continue
                print(row)

                currency_rate = CurrencyRate.objects.create(
                    date=datetime.strptime(row[0], '%Y%m%d'),
                    usd=float(row[2].replace(",", ".")),
                    eur=float(row[8].replace(",", ".")),
                    gbp=float(row[11].replace(",", ".")),
                    rub=float(row[30].replace(",", ".")) if row[30] else None,
                )
                print(currency_rate)
                # print(row)
                # result = {
                #     "date": row[0],
                #     "USD": float(row[2].replace(",", ".")),
                #     "EUR": float(row[8].replace(",", ".")),
                #     "GBP": float(row[11].replace(",", ".")),
                # }
                # print(result)

        # BROKER FILE
        elif instance.file.name.startswith("IB"):
            csvreader = csv.reader(file)
            for row in csvreader:
                row_type = row[0]

                # TRANSACTION
                if row_type == "Trades" and row[1] == "Data":
                    print(row)
                    # print("TRADE")
                    # TODO make it atomic
                    print(get_option_type(row[asset_index]))
                    is_option = row[asset_type_index] == "Equity and Index Options"
                    transaction, created = Transaction.objects.get_or_create(
                        asset=row[asset_index],
                        side="Buy" if int(row[quantity_index].replace(",", "")) > 0 else "Sell",
                        asset_type=row[asset_type_index],
                        price=float(row[price_index]),
                        quantity=int(row[quantity_index].replace(",", "")),
                        value=float(row[value_index]),
                        currency=row[currency_index],
                        fee=float(row[fee_index]),
                        option_type=get_option_type(row[asset_index]) if is_option else "",
                        strike_price=get_strike_price(row[asset_index]) if is_option else None,
                        executed_at=datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
                    )



@receiver(post_save, sender=Transaction)
def calculate_tax_to_pay(sender, instance, *args, **kwargs):
    if instance.asset_type == "Equity and Index Options":
        tax_year = instance.executed_at.year
        transaction_currency = instance.currency.lower()
        transaction_date = instance.executed_at.date()
        print(instance.executed_at.date())
        # NOTE sprawdzic czy to ze nie ma dnia w nbp kursach czy znaczy ze faktycznie bylo swieto
        previous_currency_rate = CurrencyRate.objects.filter(date__lt=transaction_date).order_by('-date').first()
        print(previous_currency_rate)

        option_premium_pln = round(instance.value * getattr(previous_currency_rate, transaction_currency), 2)
        tax_to_pay_from_transaction = round(option_premium_pln * 0.19, 2)

        previous_state, created = Tax.objects.get_or_create(year=tax_year, defaults={
            'to_pay': 0
        })
        tax, created = Tax.objects.update_or_create(
            year=instance.executed_at.year,
            defaults={
                'to_pay': previous_state.to_pay+tax_to_pay_from_transaction
            }
        )
        print(tax.to_pay)