
import re
from datetime import datetime

from transactions.models import CurrencyRate, Dividend

def _get_value_per_share(text: str) -> float | None:
    # NOTE regex catching all the floating numbers from the string
    match = re.search(re.compile(r'\b\d+(\.\d+)?\b'), text)
    if match:
        return float(match.group())
    return None

def save_dividend_object(row: list[str]):
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    received_at_index = 3

    received_at = datetime.strptime(row[received_at_index], "%Y-%m-%d")
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=received_at).order_by("-date").first()

    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value_per_share = _get_value_per_share(row[asset_name_index])
    value = round(float(row[value_index]), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    Dividend.objects.get_or_create(
        asset_name=asset_name,
        value_per_share=value_per_share,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        received_at=received_at,
    )