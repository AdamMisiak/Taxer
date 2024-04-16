import re
from datetime import datetime
from files.models import ReportFile
from utils.logic import get_previous_day_curreny_rate
from transactions.models import DividendTransaction
from utils.choices import Currency


def _get_value_per_share(text: str) -> float | None:
    # NOTE regex catching all the floating numbers from the string
    match = re.search(re.compile(r'\b\d+(\.\d+)?\b'), text)
    if match:
        return float(match.group())
    return None

def save_ib_lynx_dividend_transaction(row: list[str], report_file_object: ReportFile):
    asset_type_index = 0
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    executed_at_index = 3

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d")
    previous_day_currency_rate = get_previous_day_curreny_rate(executed_at)
    
    asset_name = row[asset_name_index].split("(")[0].strip()
    asset_type = (
        row[asset_type_index]
        .strip()
    )

    currency = getattr(Currency, row[currency_index]).value

    value_per_share = _get_value_per_share(row[asset_name_index])
    value = round(float(row[value_index]), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    DividendTransaction.objects.get_or_create(
        asset_name=asset_name,
        value_per_share=value_per_share,
        value=value,
        value_pln=value_pln,
        executed_at=executed_at,
        raw_data=str(row),
        defaults={
            "report_file": report_file_object,
            "previous_day_currency_rate": previous_day_currency_rate,
            "asset_type": asset_type,
            "currency": currency,
            "raw_data": str(row)
        }
    )
