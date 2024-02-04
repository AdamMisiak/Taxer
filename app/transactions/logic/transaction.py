from datetime import datetime, timedelta
import re
from transactions.models import CurrencyRate, Transaction, WithholdingTax

def _get_option_type(option_name: str) -> str:
    return "CALL" if option_name[-1] == "C" else "PUT"


def _get_strike_price(option_name: str) -> float:
    return float(option_name.split()[-2])

def save_trade_transaction_object(row: list[str]):
    print(row)
    asset_name_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d, %H:%M:%S") + timedelta(hours=6)
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by("-date").first()

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
    # NOTE Watch of for forex records
    price = round(float(row[price_index]), 2)
    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )
    fee = abs(float(row[fee_index]))
    is_option = asset_type == "Equity and Index Options"

    Transaction.objects.get_or_create(
        asset_name=asset_name,
        side=side,
        price=price,
        quantity=quantity,
        executed_at=executed_at,
        defaults={
            "asset_type": asset_type,
            "value": value,
            "value_pln": value_pln,
            "currency": currency,
            "previous_day_currency_rate": previous_day_currency_rate,
            "fee": fee,
            "option_type": _get_option_type(asset_name) if is_option else "",
            "strike_price": _get_strike_price(asset_name) if is_option else None,
        },
    )


def _get_value_per_share(text: str) -> float | None:
    # NOTE regex catching all the floating numbers from the string
    match = re.search(re.compile(r'\b\d+(\.\d+)?\b'), text)
    if match:
        return float(match.group())
    return None

def save_dividend_transaction_object(row: list[str]):
    asset_type_index = 0
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    executed_at_index = 3

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d")
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by("-date").first()
    
    asset_type = (
        row[asset_type_index]
        .strip()
    )
    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value_per_share = _get_value_per_share(row[asset_name_index])
    value = round(float(row[value_index]), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    Transaction.objects.get_or_create(
        asset_name=asset_name,
        asset_type=asset_type,
        value_per_share=value_per_share,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        executed_at=executed_at,
    )

def save_withholding_tax_transaction_object_ib_broker(row: list[str]):
    asset_type_index = 0
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    executed_at_index = 3

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d")
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by("-date").first()

    asset_type = (
        row[asset_type_index]
        .strip()
    )
    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value_per_share = _get_value_per_share(row[asset_name_index])
    value = round(float(row[value_index])*-1, 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )


    # TODO test that it is working fine with change of the order
    withholding_tax_object, created = Transaction.objects.get_or_create(
        asset_name=asset_name,
        asset_type=asset_type,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        executed_at=executed_at,
    )
    if created:
        value_filter = {"value__gt": 0} if value > 0 else {"value__lt": 0}
        matching_dividend_object = Transaction.objects.get(
            asset_name=asset_name,
            asset_type="Dividends",
            value_per_share=value_per_share,
            currency=currency,
            previous_day_currency_rate=previous_day_currency_rate,
            executed_at=executed_at,
            withholding_tax__isnull=True,
            **value_filter,
        )

        matching_dividend_object.withholding_tax = withholding_tax_object
        matching_dividend_object.save()