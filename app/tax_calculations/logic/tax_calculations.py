from django.conf import settings
from transactions.models import BaseTransaction
from tax_calculations.models import AssetTaxCalculation
from django.db.models import QuerySet

def calculate_tax_single_transaction_same_quantity(opening_transaction: BaseTransaction, closing_transaction: BaseTransaction):
    tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year
    profit_or_loss = round(closing_transaction.full_value_pln - opening_transaction.full_value_pln, 2)
    tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

    AssetTaxCalculation.objects.get_or_create(
        # tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=closing_transaction.full_value_pln,
        cost=opening_transaction.full_value_pln,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay_from_transaction,
    )

def calculate_tax_multiple_transactions(matching_opening_transactions: QuerySet[BaseTransaction], closing_transaction: BaseTransaction):
    for opening_transaction in matching_opening_transactions:
        opening_transaction.refresh_from_db()
        closing_transaction.refresh_from_db()

        if (
            opening_transaction.quantity == closing_transaction.quantity
            and not opening_transaction.as_opening_calculation.all()
            and not closing_transaction.as_opening_calculation.all()
        ):
            calculate_tax_single_transaction_same_quantity(
                opening_transaction=opening_transaction, closing_transaction=closing_transaction
            )
            break
        else:
            # NOTE temp
            print(f"❌ Transaction: {opening_transaction} has not been handled!")