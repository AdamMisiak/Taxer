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

# NOTE think about the name? "same" quantity?
def calculate_tax_multiple_transactions_same_quantity(
    opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
):
    # ratio = quantity / opening_transaction.quantity if quantity else 1
    # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

    # revenue = 0
    # cost = round(opening_transaction.full_value_pln * ratio, 2)

    # if quantity:
    #     profit_or_loss = round(revenue - cost, 2)
    # else:
    #     profit_or_loss = round(-opening_transaction.full_value_pln, 2)
    # tax = round(profit_or_loss * settings.TAX_RATE, 2)

    # TaxCalculation.objects.create(
    #     tax_summary=TaxSummary.objects.get(year=tax_year),
    #     opening_transaction=opening_transaction,
    #     closing_transaction=closing_transaction,
    #     revenue=revenue,
    #     cost=cost,
    #     profit_or_loss=profit_or_loss,
    #     tax=tax,
    #     quantity=quantity,
    # )
    revenue = 0
    cost = opening_transaction.full_value_pln
    profit_or_loss = round(revenue - cost, 2)
    tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)
    AssetTaxCalculation.objects.get_or_create(
        # tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay_from_transaction,
    )

# TODO refactor this names
def _get_partial_quantity_for_transaction(closing_transaction_quantity, summary_opening_transaction_quantity):
    quantity_used_in_current_transaction = closing_transaction_quantity - summary_opening_transaction_quantity
    return quantity_used_in_current_transaction

def calculate_tax_multiple_transactions(matching_opening_transactions: QuerySet[BaseTransaction], closing_transaction: BaseTransaction):
    summary_opening_transactions_quantity = 0

    for opening_transaction in matching_opening_transactions:
        if (
            opening_transaction.quantity == closing_transaction.quantity
            and not opening_transaction.as_opening_calculation.all()
            and not closing_transaction.as_opening_calculation.all()
        ):
            print(f"ℹ️  Used full transaction with matching quantity: {opening_transaction}")
            calculate_tax_single_transaction_same_quantity(
                opening_transaction=opening_transaction, closing_transaction=closing_transaction
            )
            break
        elif opening_transaction.quantity <= closing_transaction.quantity and not opening_transaction.as_opening_calculation.all():
            summary_opening_transactions_quantity += opening_transaction.quantity
            if summary_opening_transactions_quantity + opening_transaction.quantity < closing_transaction.quantity:
                print(f"ℹ️  Used partial transaction with smaller quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_multiple_transactions_same_quantity(opening_transaction=opening_transaction, closing_transaction=closing_transaction)
            elif summary_opening_transactions_quantity + opening_transaction.quantity == closing_transaction.quantity:
                print(f"ℹ️  Used partial last transaction with matching quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_single_transaction_same_quantity(
                    opening_transaction=opening_transaction, closing_transaction=closing_transaction
                )
            elif summary_opening_transactions_quantity + opening_transaction.quantity > closing_transaction.quantity:
                print(" I AM HERE")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                print(summary_opening_transactions_quantity)
                print(opening_transaction.quantity)
                print(closing_transaction.quantity)
                # NOTE next handle AMT use case with 19 (?) + 100 stocks
                # if summary_opening_transactions_quantity + opening_transaction.quantity > closing_transaction.quantity:
                # something is wrong with AMT transactions - using this "Used full transaction with matching quantity" 
            
            #     quantity = _get_partial_quantity_for_transaction(
            #         closing_transaction.quantity, summary_opening_transaction_quantity
            #     )
            #     print(f"ℹ️  Used last partial transaction with {quantity} quantity: {transaction}")
            #     _calculate_tax_equity_partial_different_quantity(transaction, closing_transaction, quantity)
            #     break
            # else:
            #     summary_opening_transaction_quantity += opening_transaction.quantity
            #     print(f"ℹ️  Used middle transaction: {transaction}")
            #     _calculate_tax_equity_partial_different_quantity(transaction, closing_transaction)
        else:
            # NOTE temp
            print(f"❌ Transaction: {opening_transaction} has not been handled!")