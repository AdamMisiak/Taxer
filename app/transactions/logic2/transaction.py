from datetime import datetime, timedelta
import re
from rates.models import CurrencyRate
from utils.logic import get_previous_day_curreny_rate
from transactions.models import AssetTransaction
from django.contrib.auth.models import User
# from transactions.models import CurrencyRate, Transaction, WithholdingTax

def save_ib_lynx_transaction(row: list[str]):
    asset_name_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d, %H:%M:%S") + timedelta(hours=6)
    # NOTE filter by curreny also?
    previous_day_currency_rate = get_previous_day_curreny_rate(executed_at)
    # NOTE how to get user here?
    user = User.objects.get(email="admin@admin.com")

    asset_name = row[asset_name_index]
    asset_type = (
        row[asset_type_index]
        .replace(
            " - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC",
            "",
        )
        .strip()
    )
    # Creating raw quantity (negative or positive) to determine side of the transaction
    quantity_raw = float(row[quantity_index].replace(",", ""))
    side = "Buy" if quantity_raw > 0 else "Sell"
    quantity = abs(quantity_raw)
    currency = row[currency_index]
    price = round(float(row[price_index]), 2)
    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )
    fee = abs(float(row[fee_index]))
    full_value = round(value + fee, 2) if side == "Buy" else round(value - fee, 2)
    full_value_pln = (
        round(full_value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else full_value
    )

    AssetTransaction.objects.get_or_create(
        asset_name=asset_name,
        side=side,
        price=price,
        quantity=quantity,
        executed_at=executed_at,
        defaults={
            "user": user,
            "asset_type": asset_type,
            "value": value,
            "full_value": full_value,
            "value_pln": value_pln,
            "full_value_pln": full_value_pln,
            "currency": currency,
            # NOTE something is failing here
            # "previous_day_currency_rate": previous_day_currency_rate,
            "fee": fee,
        },
    )