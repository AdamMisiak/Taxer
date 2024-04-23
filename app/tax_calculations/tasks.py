from celery import shared_task
from files.models import ReportFile, CurrencyRateFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file
from tax_calculations.models import AssetTaxCalculation
from transactions.models import AssetTransaction
from utils.exceptions import ImportException
from utils.choices import TransactionSide
from tax_calculations.logic import create_asset_tax_calculations

broker_name_mapping = {
    settings.INTERACTIVE_BROKERS: save_data_ib_lynx_report_file,
    settings.LYNX: save_data_ib_lynx_report_file,
}

@shared_task
def create_tax_calculations():
    print("⚡️ Celery task: create_tax_calculations function started.")

    # NOTE maybe add dict with key = transaction type and value = function reference
    sell_transactions_without_calculations = AssetTransaction.objects.filter(side=TransactionSide.SELL.value).order_by("executed_at")
    for sell_transaction in sell_transactions_without_calculations:
        create_asset_tax_calculations(sell_transaction)

