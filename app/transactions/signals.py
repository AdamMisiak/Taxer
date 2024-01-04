
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from datetime import datetime, timedelta
from transactions.models import ImportFile, Transaction


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
    datetime_index = 6

    with instance.file.open('r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            row_type = row[0]

            # TRANSACTION
            if row_type == "Trades" and row[1] == "Data":
                print(row)
                # print("TRADE")
                
                print(get_option_type(row[asset_index]))
                is_option = row[asset_type_index] == "Equity and Index Options"
                transaction, created = Transaction.objects.get_or_create(
                    asset=row[asset_index],
                    side="Buy" if int(row[quantity_index]) > 0 else "Sell",
                    asset_type=row[asset_type_index],
                    price=float(row[price_index]),
                    quantity=int(row[quantity_index]),
                    value=float(row[value_index]),
                    currency=row[currency_index],
                    fee=float(row[fee_index]),
                    option_type=get_option_type(row[asset_index]) if is_option else "",
                    strike_price=get_strike_price(row[asset_index]) if is_option else None,
                    datetime=datetime.strptime(row[datetime_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
                )

