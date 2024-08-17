from celery import shared_task
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file
from transactions.models import AssetTransaction, DividendTransaction, OptionTransaction
from tax_calculations.logic import create_asset_tax_calculations, create_dividend_tax_calculations, create_option_tax_calculations
from utils.choices import TransactionType

broker_name_mapping = {
    settings.INTERACTIVE_BROKERS: save_data_ib_lynx_report_file,
    settings.LYNX: save_data_ib_lynx_report_file,
}

@shared_task
def create_tax_calculations():
    print("⚡️ Celery task: create_tax_calculations function started.")

    # NOTE check how , as_closing_calculation__isnull=True is working (czy zadziala dla tych z quantity, jesli nie to zrobic OR w query i pokryc ten use case)
    print('➡️  Assets: \n')
    sell_transactions_without_calculations = AssetTransaction.objects.filter(type=TransactionType.CLOSING.value, as_closing_calculation__isnull=True).order_by("executed_at")
    for sell_transaction in sell_transactions_without_calculations:
        create_asset_tax_calculations(sell_transaction)

    print('➡️  Dividends: \n')
    dividend_transactions_without_calculations = DividendTransaction.objects.filter(tax_calculation__isnull=True).order_by("executed_at")
    for dividend_transaction in dividend_transactions_without_calculations:
        create_dividend_tax_calculations(dividend_transaction)

    print('➡️  Options: \n')
    option_transactions_without_calculations = OptionTransaction.objects.filter(type=TransactionType.CLOSING.value, as_closing_calculation__isnull=True, as_opening_calculation__isnull=True).order_by("executed_at")
    for option_transaction in option_transactions_without_calculations:
        create_option_tax_calculations(option_transaction)