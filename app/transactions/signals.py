
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

        # NOTE close those in separated functions in logic file?
        # RATES FILE
        if instance.file.name.startswith("Rates"):
            csvreader = csv.reader(file, delimiter=';')
            for row in csvreader:
                if len(row) == 0 or not re.match(r"^([\d]+)$", row[0]):
                    continue
                print(row)

                currency_rate, created = CurrencyRate.objects.get_or_create(
                    date=datetime.strptime(row[0], '%Y%m%d'),
                    defaults = {
                        "usd": float(row[2].replace(",", ".")),
                        "eur": float(row[8].replace(",", ".")),
                        "gbp": float(row[11].replace(",", ".")),
                        "rub": float(row[30].replace(",", ".")) if row[30] else None,
                    }
                )
                print(currency_rate)

        # BROKER FILE
        elif instance.file.name.startswith("IB"):
            csvreader = csv.reader(file)
            for row in csvreader:
                row_type = row[0]

                # TRANSACTION
                if row_type == "Trades" and row[1] == "Data":
                    print(row)
                    # if jest numer konta to go usun
                    if row[5].startswith("U"):
                        del row[5]

                    # print("TRADE")
                    # TODO make it atomic
                    formatted_asset_type = row[asset_type_index].replace(" - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC", "").strip()
                    print(formatted_asset_type)
                    is_option = formatted_asset_type in ["Equity and Index Options"]
                    executed_at = datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
                    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by('-date').first()
                    transaction, created = Transaction.objects.get_or_create(
                        asset=row[asset_index],
                        side="Buy" if float(row[quantity_index].replace(",", "")) > 0 else "Sell",
                        # asset_type=row[asset_type_index],
                        price=float(row[price_index]),
                        quantity=float(row[quantity_index].replace(",", "")),
                        # value=float(row[value_index]),
                        # currency=row[currency_index],
                        # fee=float(row[fee_index]),
                        # option_type=get_option_type(row[asset_index]) if is_option else "",
                        # strike_price=get_strike_price(row[asset_index]) if is_option else None,
                        executed_at=datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6),
                        defaults={
                            'asset_type': formatted_asset_type,
                            'value': float(row[value_index]),
                            'value_pln': round(float(row[value_index]) * getattr(previous_day_currency_rate, row[currency_index].lower()), 2) if row[currency_index].lower() != "pln" else float(row[value_index]),
                            'currency': row[currency_index],
                            'previous_day_currency_rate': previous_day_currency_rate,
                            'fee': float(row[fee_index]),
                            'option_type': get_option_type(row[asset_index]) if is_option else "",
                            'strike_price': get_strike_price(row[asset_index]) if is_option else None,
                        }
                    )

def increase_tax_to_pay(tax_year, increased_by):
    previous_state, created = Tax.objects.get_or_create(year=tax_year, defaults={
        'to_pay': 0
    })
    tax, created = Tax.objects.update_or_create(
        year=tax_year,
        defaults={
            'to_pay': previous_state.to_pay+increased_by
        }
    )
    print(tax.to_pay)


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
        tax_to_pay_from_transaction = round(option_premium_pln * 0.19, 2)

        print(tax_year)
        increase_tax_to_pay(tax_year, tax_to_pay_from_transaction)

    elif instance.asset_type == "Stocks" and instance.side == "Sell":
        print(instance)
        matching_transactions = Transaction.objects.filter(asset=instance.asset, side="Buy").order_by("executed_at")
        print(matching_transactions)
        # NOTE gdzie zapisywac info ze transakcja juz rozliczona? nowy model match transakcji?
        if len(matching_transactions) == 1:
            if matching_transactions[0].quantity == instance.quantity:
                print('calucalte tax here!')


        tax_to_pay_from_transaction = 5
        increase_tax_to_pay(tax_year, tax_to_pay_from_transaction)
