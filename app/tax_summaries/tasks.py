from celery import shared_task
from files.models import ReportFile, CurrencyRateFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file
from tax_calculations.models import AssetTaxCalculation
from transactions.models import AssetTransaction, DividendTransaction, OptionTransaction
from utils.exceptions import ImportException
from utils.choices import TransactionSide
from tax_summaries.logic import assign_asset_tax_summary
from utils.choices import TransactionSide, TransactionType
from tax_calculations.models import AssetTaxCalculation
broker_name_mapping = {
    settings.INTERACTIVE_BROKERS: save_data_ib_lynx_report_file,
    settings.LYNX: save_data_ib_lynx_report_file,
}

@shared_task
def create_tax_summaries():
    print("⚡️ Celery task: create_tax_summaries function started.")

    print('➡️  Assets: \n')
    tax_calculations_without_summary = AssetTaxCalculation.objects.filter(tax_summary__isnull=True).order_by("closing_transaction__executed_at")
    for tax_calculation in tax_calculations_without_summary:
        print(tax_calculation)
        assign_asset_tax_summary(tax_calculation)







    # print('➡️  Dividends: \n')
    # dividend_transactions_without_calculations = DividendTransaction.objects.filter(tax_calculation__isnull=True).order_by("executed_at")
    # for dividend_transaction in dividend_transactions_without_calculations:
    #     create_dividend_tax_calculations(dividend_transaction)

    # print('➡️  Options: \n')
    # option_transactions_without_calculations = OptionTransaction.objects.filter(type=TransactionType.CLOSING.value, as_closing_calculation__isnull=True, as_opening_calculation__isnull=True).order_by("executed_at")
    # for option_transaction in option_transactions_without_calculations:
    #     create_option_tax_calculations(option_transaction)