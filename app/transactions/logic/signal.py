

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
            # csvreader = csv.reader(file)
            # for row in csvreader:
            #     row_type = row[0]

            #     # TRANSACTION
            #     if row_type == "Trades" and row[1] == "Data":
            #         print(row)
            #         # if jest numer konta to go usun
            #         if row[5].startswith("U"):
            #             del row[5]

            #         # print("TRADE")
            #         # TODO make it atomic
            #         formatted_asset_type = row[asset_type_index].replace(" - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC", "").strip()
            #         print(formatted_asset_type)
            #         is_option = formatted_asset_type in ["Equity and Index Options"]
            #         executed_at = datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
            #         previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by('-date').first()
            #         transaction, created = Transaction.objects.get_or_create(
            #             asset=row[asset_index],
            #             side="Buy" if float(row[quantity_index].replace(",", "")) > 0 else "Sell",
            #             # asset_type=row[asset_type_index],
            #             price=float(row[price_index]),
            #             quantity=float(row[quantity_index].replace(",", "")),
            #             # value=float(row[value_index]),
            #             # currency=row[currency_index],
            #             # fee=float(row[fee_index]),
            #             # option_type=get_option_type(row[asset_index]) if is_option else "",
            #             # strike_price=get_strike_price(row[asset_index]) if is_option else None,
            #             executed_at=datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6),
            #             defaults={
            #                 'asset_type': formatted_asset_type,
            #                 'value': float(row[value_index]),
            #                 'value_pln': round(float(row[value_index]) * getattr(previous_day_currency_rate, row[currency_index].lower()), 2) if row[currency_index].lower() != "pln" else float(row[value_index]),
            #                 'currency': row[currency_index],
            #                 'previous_day_currency_rate': previous_day_currency_rate,
            #                 'fee': float(row[fee_index]),
            #                 'option_type': get_option_type(row[asset_index]) if is_option else "",
            #                 'strike_price': get_strike_price(row[asset_index]) if is_option else None,
            #             }
            #         )
