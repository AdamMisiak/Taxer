from django.conf import settings
from transactions.models import BaseTransaction
from tax_calculations.models import AssetTaxCalculation

def calculate_tax_equity_same_quantity(opening_transaction: BaseTransaction, closing_transaction: BaseTransaction):
    tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year
    profit_or_loss = round(closing_transaction.full_value_pln - opening_transaction.full_value_pln, 2)
    tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)
    print(profit_or_loss)
    print(tax_to_pay_from_transaction)

    AssetTaxCalculation.objects.get_or_create(
        # tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=closing_transaction.full_value_pln,
        cost=opening_transaction.full_value_pln,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay_from_transaction,
    )