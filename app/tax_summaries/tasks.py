from celery import shared_task
from files.models import ReportFile, CurrencyRateFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file
from tax_calculations.models import AssetTaxCalculation
from transactions.models import AssetTransaction, DividendTransaction, OptionTransaction
from utils.exceptions import ImportException
from utils.choices import TransactionSide
from tax_summaries.logic import assign_asset_tax_summary, assign_option_tax_summary, assign_dividend_tax_summary, assign_general_tax_summary
from utils.choices import TransactionSide, TransactionType
from tax_calculations.models import AssetTaxCalculation, OptionTaxCalculation, DividendTaxCalculation
from tax_summaries.models import AssetTaxSummary, DividendTaxSummary, OptionTaxSummary

@shared_task
def create_tax_summaries():
    print("⚡️ Celery task: create_tax_summaries function started.")

    print('➡️  Assets: \n')
    asset_tax_calculations_without_summary = AssetTaxCalculation.objects.filter(tax_summary__isnull=True).order_by("closing_transaction__executed_at")
    for tax_calculation in asset_tax_calculations_without_summary:
        print(tax_calculation)
        assign_asset_tax_summary(tax_calculation)

    print('➡️  Dividends: \n')
    dividend_tax_calculations_without_summary = DividendTaxCalculation.objects.filter(tax_summary__isnull=True).order_by("dividend_transaction__executed_at")
    for tax_calculation in dividend_tax_calculations_without_summary:
        print(tax_calculation)
        assign_dividend_tax_summary(tax_calculation)

    print('➡️  Options: \n')
    option_tax_calculations_without_summary = OptionTaxCalculation.objects.filter(tax_summary__isnull=True).order_by("closing_transaction__executed_at")
    for tax_calculation in option_tax_calculations_without_summary:
        print(tax_calculation)
        assign_option_tax_summary(tax_calculation)

    print('➡️  General: \n')
    tax_summaries_without_general_summary = AssetTaxSummary.objects.filter(general_tax_summary__isnull=True)
    # tax_summaries_without_general_summary = AssetTaxSummary.objects.filter(general_tax_summary__isnull=True) | DividendTaxSummary.objects.filter(general_tax_summary__isnull=True) | OptionTaxSummary.objects.filter(general_tax_summary__isnull=True)
    for tax_summary in tax_summaries_without_general_summary:
        print(tax_summary)
        assign_general_tax_summary(tax_summary)
    # option_tax_calculations_without_summary = OptionTaxCalculation.objects.filter(tax_summary__isnull=True).order_by("closing_transaction__executed_at")
    # for tax_calculation in option_tax_calculations_without_summary:
    #     print(tax_calculation)
    #     assign_option_tax_summary(tax_calculation)