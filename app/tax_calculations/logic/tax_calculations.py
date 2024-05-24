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

def calculate_tax_multiple_transactions_different_quantity(
    opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
):
    ratio = quantity / opening_transaction.quantity
    # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

    revenue = round(closing_transaction.full_value_pln, 2)
    cost = round(opening_transaction.full_value_pln * ratio, 2)
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
        quantity=quantity,
    )

def calculate_tax_first_of_many_transactions_with_quantity(
    opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
):
    ratio = quantity / opening_transaction.quantity
    # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

    revenue = 0
    cost = round(opening_transaction.full_value_pln * ratio, 2)
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
        quantity=quantity,
    )

def calculate_tax_multiple_transactions(matching_opening_transactions: QuerySet[BaseTransaction], closing_transaction: BaseTransaction):
    summary_opening_transactions_quantity = 0

    for opening_transaction in matching_opening_transactions:
        if (
            summary_opening_transactions_quantity == 0
            and opening_transaction.quantity == closing_transaction.quantity
            and not opening_transaction.as_opening_calculation.all()
            and not closing_transaction.as_opening_calculation.all()
        ):
            print(f"ℹ️  Used full transaction with matching quantity: {opening_transaction}")
            calculate_tax_single_transaction_same_quantity(
                opening_transaction=opening_transaction, closing_transaction=closing_transaction
            )
            break

        elif opening_transaction.quantity <= closing_transaction.quantity and not opening_transaction.as_opening_calculation.all():
            if summary_opening_transactions_quantity + opening_transaction.quantity < closing_transaction.quantity:
                summary_opening_transactions_quantity += opening_transaction.quantity
                print(f"ℹ️  Used (partial) middle transaction with smaller quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_multiple_transactions_same_quantity(opening_transaction=opening_transaction, closing_transaction=closing_transaction)
            
            elif summary_opening_transactions_quantity + opening_transaction.quantity == closing_transaction.quantity:
                summary_opening_transactions_quantity += opening_transaction.quantity
                print(f"ℹ️  Used (partial) last transaction with matching quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_single_transaction_same_quantity(
                    opening_transaction=opening_transaction, closing_transaction=closing_transaction
                )
            
            elif summary_opening_transactions_quantity < closing_transaction.quantity and summary_opening_transactions_quantity + opening_transaction.quantity > closing_transaction.quantity:
                remaining_quantity = closing_transaction.quantity - summary_opening_transactions_quantity
                summary_opening_transactions_quantity += remaining_quantity
                print(f"ℹ️  Used (partial) last transaction with smaller quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_multiple_transactions_different_quantity(opening_transaction=opening_transaction, closing_transaction=closing_transaction, quantity=remaining_quantity)

        elif opening_transaction.quantity <= closing_transaction.quantity and opening_transaction.as_opening_calculation.all() and opening_transaction.as_opening_calculation.last().quantity:
            remaining_quantity = opening_transaction.quantity - opening_transaction.as_opening_calculation.last().quantity
            summary_opening_transactions_quantity += remaining_quantity
            print(f"ℹ️  Used (partial) first? transaction with smaller quantity: {opening_transaction}")
            print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
            calculate_tax_first_of_many_transactions_with_quantity(opening_transaction=opening_transaction, closing_transaction=closing_transaction, quantity=remaining_quantity)
            

            # NOTE check if all transacations are covered + proper checking for 2020-2023 transactions
        
        elif opening_transaction.as_opening_calculation.all() and not opening_transaction.as_opening_calculation.last().quantity:
            print(f"ℹ️  Transaction: {opening_transaction} was already used in the calculations!")

        else:
            # NOTE temp
            print(f"❌ Transaction: {opening_transaction} has not been handled!")