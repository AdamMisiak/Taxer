import csv
from datetime import datetime, timedelta
from transactions.models import Transaction, CurrencyRate


def _get_option_type(option_name: str) -> str:
    return "CALL" if option_name[-1] == "C" else "PUT"

def _get_strike_price(option_name: str) -> float:
    return float(option_name.split()[-2])

def _save_transaction_object(row):
    asset_name_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6

    executed_at = datetime.strptime(row[executed_at_index], '%Y-%m-%d, %H:%M:%S') + timedelta(hours=6)
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by('-date').first()

    asset_name = row[asset_name_index]
    asset_type = row[asset_type_index].replace(" - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC", "").strip()
    quantity = float(row[quantity_index].replace(',',''))
    side = "Buy" if quantity > 0 else "Sell"
    currency = row[currency_index]
    price = float(row[price_index])
    value = float(row[value_index])
    value_pln = round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if row[currency_index].lower() != "pln" else value
    fee = float(row[fee_index])
    is_option = asset_type == "Equity and Index Options"

    Transaction.objects.get_or_create(
        asset_name=asset_name,
        side=side,
        price=price,
        quantity=quantity,
        executed_at=executed_at,
        defaults={
            'asset_type': asset_type,
            'value': value,
            'value_pln': value_pln,
            'currency': currency,
            'previous_day_currency_rate': previous_day_currency_rate,
            'fee': fee,
            'option_type': _get_option_type(asset_name) if is_option else "",
            'strike_price': _get_strike_price(asset_name) if is_option else None,
        }
    )



def save_data_ib_broker_file(file):
    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]

        # TRANSACTION
        if row_type == "Trades" and row[1] == "Data":
            if row[5].startswith("U"):
                del row[5]

            # TODO make it atomic?
            _save_transaction_object(row)

        # DIVIDEND
        elif row_type == "Dividend":
            pass
