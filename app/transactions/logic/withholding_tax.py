import csv
import re
from datetime import datetime, timedelta

from transactions.models import CurrencyRate, Transaction, Dividend, WithholdingTax

def save_withholding_tax_object(row: list[str]):
    from transactions.logic import _get_value_per_share

    asset_name_index = 4
    value_index = 5
    currency_index = 2
    paid_at_index = 3


    paid_at = datetime.strptime(row[paid_at_index], "%Y-%m-%d")
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=paid_at).order_by("-date").first()

    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value_per_share = _get_value_per_share(row[asset_name_index])
    value = round(float(row[value_index])*-1, 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    value_filter = {"value__gt": 0} if value > 0 else {"value__lt": 0}
    matching_dividend_object = Dividend.objects.get(
        asset_name=asset_name,
        value_per_share=value_per_share,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        received_at=paid_at,
        withholding_tax__isnull=True,
        **value_filter,
    )

    withholding_tax_object, created = WithholdingTax.objects.get_or_create(
        asset_name=asset_name,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        paid_at=paid_at,
    )

    matching_dividend_object.withholding_tax = withholding_tax_object
    matching_dividend_object.save()
