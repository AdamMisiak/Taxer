from transactions.models import DividendTransaction, WithholdingTaxTransaction
from tax_calculations.models import DividendTaxCalculation
from datetime import timedelta
from django.conf import settings
from utils.choices import TransactionSide


def create_dividend_tax_calculations(dividend_transaction: DividendTransaction):
    # from tax_calculations.logic import calculate_tax_single_transaction_same_quantity, calculate_tax_multiple_transactions

    withholding_tax_transaction = dividend_transaction.withholding_tax_transaction
    if withholding_tax_transaction:

        tax_year = dividend_transaction.executed_at.year
        asset_name = dividend_transaction.asset_name

        dividend_pln = round(dividend_transaction.value_pln, 2)
        withholding_tax_pln = round(withholding_tax_transaction.value_pln, 2)
        dividend_net = round(dividend_pln - withholding_tax_pln, 2)

        tax_rate = settings.CUSTOM_DIVIDEND_RATES.get(asset_name, settings.TAX_RATE)
        tax_to_pay_from_dividend = round((dividend_pln * tax_rate) - withholding_tax_pln, 2)

        # init_tax_summary(tax_year)

        DividendTaxCalculation.objects.create(
            # tax_summary=TaxSummary.objects.get(year=tax_year),
            withholding_tax_transaction=withholding_tax_transaction,
            dividend_transaction=dividend_transaction,
            revenue=dividend_pln,
            cost=withholding_tax_pln,
            profit_or_loss=dividend_net,
            tax=tax_to_pay_from_dividend,
            tax_rate=tax_rate,
        )
    else:
        print(f"❌ Withholding tax transaction is missing for {dividend_transaction}")