from datetime import datetime, timedelta
from utils.logic import get_previous_day_curreny_rate
from transactions.models import InterestRateTransaction
from files.models import ReportFile
from utils.choices import AssetType, TransactionSide

def save_ib_lynx_interest_rate_transaction_object(row: list[str], report_file_object: ReportFile):
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    executed_at_index = 3

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d") + timedelta(hours=6)
    previous_day_currency_rate = get_previous_day_curreny_rate(executed_at)

    asset_name = row[asset_name_index]
    currency = row[currency_index]

    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    InterestRateTransaction.objects.get_or_create(
        asset_name=asset_name,
        asset_type=AssetType.OTHERS.value,
        currency=currency,
        side=TransactionSide.BUY.value,
        value=value,
        value_pln=value_pln,
        executed_at=executed_at,
        defaults={
            "report_file": report_file_object,
            "previous_day_currency_rate": previous_day_currency_rate,
            "raw_data": str(row)
        },
    )
