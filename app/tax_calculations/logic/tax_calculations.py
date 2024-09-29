from django.conf import settings
from transactions.models import BaseTransaction, OptionTransaction
from tax_calculations.models import AssetTaxCalculation, OptionTaxCalculation
from django.db.models import QuerySet
from utils.choices import TransactionSide, TransactionType



def calculate_tax_for_complete_transaction(model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction):
    """
    Calculate tax for a complete transaction where the opening and closing transactions have the same quantity.

    Example Use Case:
    - Buying 10 shares and then selling the same 10 shares.
    - Selling 10 shares short and then buying back the same 10 shares.
    """
    if opening_transaction.side == TransactionSide.BUY:
        cost = round(opening_transaction.full_value_pln, 2)
        revenue = round(closing_transaction.full_value_pln, 2)
    else:
        cost = round(closing_transaction.full_value_pln, 2)
        revenue = round(opening_transaction.full_value_pln, 2)

    profit_or_loss = round(revenue - cost, 2)
    tax_to_pay = round(profit_or_loss * settings.TAX_RATE, 2)

    model.objects.create(
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay,
    )

def calculate_tax_for_last_partial_transaction_with_different_quantity(model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int):
    """
    Calculate tax for the last partial transaction in a series with different quantity.

    Example Use Case:
    - Buying 5 shares and then selling 4 shares. Buying 4 more shares and then selling all 5 remaining shares.
        - Calculating here BUY of 5 shares from first transaction and SELL of 4 shares.
    - Selling 5 shares short and then buying back 4 shares. Selling 4 more shares short and then buying back all 5 remaining shares.
        - Calculating here SELL short of 5 shares share from first transaction and BUY back of 4 shares.
    """
    ratio = quantity / opening_transaction.quantity

    if opening_transaction.side == TransactionSide.BUY:
        cost = round(opening_transaction.full_value_pln * ratio, 2)
        revenue = round(closing_transaction.full_value_pln, 2)
    else:
        cost = round(closing_transaction.full_value_pln, 2)
        revenue = round(opening_transaction.full_value_pln * ratio, 2)

    profit_or_loss = round(revenue - cost, 2)
    tax_to_pay = round(profit_or_loss * settings.TAX_RATE, 2)

    model.objects.create(
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay,
        quantity=quantity,
    )


def calculate_tax_for_first_partial_transaction_with_aligned_quantity(model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction):
    """
    Calculate tax for the first partial transaction in a series with aligned quantity.

    Example Use Case:
    - Buying 5 shares in two separated transactions and then selling 10 shares.
        - Calculating here BUY of first 5 shares (with revenue = 0) and SELL of all 10 shares.
    - Selling 5 shares short in two separated transactions and then buying back 10 shares.
        - Calculating here SELL short of first 5 shares (with cost = 0) and BUY back of all 10 shares.
    """
    if opening_transaction.side == TransactionSide.BUY:
        cost = round(opening_transaction.full_value_pln, 2)
        revenue = 0
    else:
        cost = 0
        revenue = round(opening_transaction.full_value_pln, 2)

    profit_or_loss = round(revenue - cost, 2)
    tax_to_pay = round(profit_or_loss * settings.TAX_RATE, 2)

    model.objects.create(
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay,
    )


def calculate_tax_for_first_partial_transaction_with_different_quantity(model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int):
    """
    Calculate tax for the first partial transaction in a series with different quantity.

    Example Use Case:
    - Buying 5 shares and then selling 4 shares. Buying 4 more shares and then selling all 5 remaining shares.
        - Calculating here BUY of remaining 1 share from first transaction and SELL of all 5 shares.
    - Selling 5 shares short and then buying back 4 shares. Selling 4 more shares short and then buying back all 5 remaining shares.
        - Calculating here SELL short of remaining 1 share from first transaction and BUY back of all 5 shares.
    """
    ratio = quantity / opening_transaction.quantity

    if opening_transaction.side == TransactionSide.BUY:
        cost = round(opening_transaction.full_value_pln * ratio, 2)
        revenue = 0
    else:
        cost = 0
        revenue = round(opening_transaction.full_value_pln * ratio, 2)

    profit_or_loss = round(revenue - cost, 2)
    tax_to_pay = round(profit_or_loss * settings.TAX_RATE, 2)

    model.objects.create(
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay,
        quantity=quantity,
    )

# -------------------------------


# NOTE those are previous version of those functions from above 


# def calculate_tax_single_transaction_same_quantity(model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction):
#     # NOTE add docstrings from gpt here 
#     if opening_transaction.side == TransactionSide.BUY:
#         revenue = round(closing_transaction.full_value_pln, 2)
#         cost = round(opening_transaction.full_value_pln, 2)
#     else:
#         revenue = round(opening_transaction.full_value_pln, 2)
#         cost = round(closing_transaction.full_value_pln, 2)

#     profit_or_loss = round(revenue - cost, 2)
#     tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

#     model.objects.get_or_create(
#         # tax_summary=TaxSummary.objects.get(year=tax_year),
#         opening_transaction=opening_transaction,
#         closing_transaction=closing_transaction,
#         revenue=revenue,
#         cost=cost,
#         profit_or_loss=profit_or_loss,
#         tax=tax_to_pay_from_transaction,
#     )

# # NOTE think about the name? "same" quantity? Take names from gpt
# def calculate_tax_multiple_transactions_same_quantity(
#     model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
# ):
#     if opening_transaction.side == TransactionSide.BUY:
#         revenue = 0
#         cost = round(opening_transaction.full_value_pln, 2)
#     else:
#         revenue = round(opening_transaction.full_value_pln, 2)
#         cost = 0

#     profit_or_loss = round(revenue - cost, 2)
#     tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

#     model.objects.get_or_create(
#         # tax_summary=TaxSummary.objects.get(year=tax_year),
#         opening_transaction=opening_transaction,
#         closing_transaction=closing_transaction,
#         revenue=revenue,
#         cost=cost,
#         profit_or_loss=profit_or_loss,
#         tax=tax_to_pay_from_transaction,
#     )

# def calculate_tax_multiple_transactions_different_quantity(
#     model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
# ):
#     ratio = quantity / opening_transaction.quantity
#     # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

#     if opening_transaction.side == TransactionSide.BUY:
#         revenue = round(closing_transaction.full_value_pln, 2)
#         cost = round(opening_transaction.full_value_pln * ratio, 2)
#     else:
#         revenue = round(opening_transaction.full_value_pln * ratio, 2)
#         cost = round(closing_transaction.full_value_pln, 2)

#     profit_or_loss = round(revenue - cost, 2)
#     tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

#     model.objects.get_or_create(
#         # tax_summary=TaxSummary.objects.get(year=tax_year),
#         opening_transaction=opening_transaction,
#         closing_transaction=closing_transaction,
#         revenue=revenue,
#         cost=cost,
#         profit_or_loss=profit_or_loss,
#         tax=tax_to_pay_from_transaction,
#         quantity=quantity,
#     )

# def calculate_tax_first_of_many_transactions_with_quantity(
#     model: BaseTransaction, opening_transaction: BaseTransaction, closing_transaction: BaseTransaction, quantity: int = None
# ):
#     ratio = quantity / opening_transaction.quantity
#     # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

#     revenue = 0
#     cost = round(opening_transaction.full_value_pln * ratio, 2)
#     profit_or_loss = round(revenue - cost, 2)
#     tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

#     model.objects.get_or_create(
#         # tax_summary=TaxSummary.objects.get(year=tax_year),
#         opening_transaction=opening_transaction,
#         closing_transaction=closing_transaction,
#         revenue=revenue,
#         cost=cost,
#         profit_or_loss=profit_or_loss,
#         tax=tax_to_pay_from_transaction,
#         quantity=quantity,
#     )




# NOTE
# check if calculations are ok comparing to previous method
# start from 2020

# add new interest rate models + relations with others to the admin panel





# NOTE adjust prints to in if statements. Those are wrong now
def calculate_tax_multiple_transactions(model: BaseTransaction, matching_opening_transactions: QuerySet[BaseTransaction], closing_transaction: BaseTransaction):
    summary_opening_transactions_quantity = 0

    for opening_transaction in matching_opening_transactions:

        if (
            summary_opening_transactions_quantity == 0
            and opening_transaction.quantity == closing_transaction.quantity
            and not opening_transaction.as_opening_calculation.all()
            and not closing_transaction.as_opening_calculation.all()
        ):
            print(f"ℹ️  Used full transaction with matching quantity: {opening_transaction}")
            calculate_tax_for_complete_transaction(
                model=model, opening_transaction=opening_transaction, closing_transaction=closing_transaction
            )
            break

        elif opening_transaction.quantity <= closing_transaction.quantity and not opening_transaction.as_opening_calculation.all():
            if summary_opening_transactions_quantity + opening_transaction.quantity < closing_transaction.quantity:
                summary_opening_transactions_quantity += opening_transaction.quantity
                print(f"ℹ️  Used (partial) middle transaction with smaller quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_for_first_partial_transaction_with_aligned_quantity(model=model, opening_transaction=opening_transaction, closing_transaction=closing_transaction)
            
            elif summary_opening_transactions_quantity + opening_transaction.quantity == closing_transaction.quantity:
                summary_opening_transactions_quantity += opening_transaction.quantity
                print(f"ℹ️  Used (partial) last transaction with matching quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_for_complete_transaction(
                    model=model, opening_transaction=opening_transaction, closing_transaction=closing_transaction
                )
            
            elif summary_opening_transactions_quantity < closing_transaction.quantity and summary_opening_transactions_quantity + opening_transaction.quantity > closing_transaction.quantity:
                remaining_quantity = closing_transaction.quantity - summary_opening_transactions_quantity
                summary_opening_transactions_quantity += remaining_quantity
                print(f"ℹ️  Used (partial) last transaction with smaller quantity: {opening_transaction}")
                print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
                calculate_tax_for_last_partial_transaction_with_different_quantity(model=model, opening_transaction=opening_transaction, closing_transaction=closing_transaction, quantity=remaining_quantity)

        elif opening_transaction.quantity <= closing_transaction.quantity and opening_transaction.as_opening_calculation.all() and opening_transaction.as_opening_calculation.last().quantity:
            remaining_quantity = opening_transaction.quantity - opening_transaction.as_opening_calculation.last().quantity
            summary_opening_transactions_quantity += remaining_quantity
            print(f"ℹ️  Used (partial) first? transaction with smaller quantity: {opening_transaction}")
            print(f"ℹ️  Summary opening transactions quantity: {summary_opening_transactions_quantity}/{closing_transaction.quantity}")
            calculate_tax_for_first_partial_transaction_with_different_quantity(model=model, opening_transaction=opening_transaction, closing_transaction=closing_transaction, quantity=remaining_quantity)
            
        elif opening_transaction.as_opening_calculation.all() and not opening_transaction.as_opening_calculation.last().quantity:
            print(f"ℹ️  Transaction: {opening_transaction} was already used in the calculations!")

        else:
            print(f"❌ Transaction: {closing_transaction} has not matching opening transactions!")

# NOTE leaving all the commented out code just in case 



# NOTE not needed? Can be replaced with general use one
# Options
# Is it needed when fucntions above are generic?
# def calculate_tax_single_transaction_same_quantity_options(opening_transaction: OptionTransaction, closing_transaction: OptionTransaction):
#     tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year
#     profit_or_loss = round(opening_transaction.full_value_pln - closing_transaction.full_value_pln, 2)
#     tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

#     if opening_transaction.side == TransactionSide.BUY:
#         revenue = round(closing_transaction.full_value_pln, 2)
#         cost = round(opening_transaction.full_value_pln, 2)
#     else:
#         revenue = round(opening_transaction.full_value_pln, 2)
#         cost = round(closing_transaction.full_value_pln, 2)

#     # NOTE is some needed check which transactions should be used for opening and closing?
#     # depending on the BUY and SELL of the option?
#     OptionTaxCalculation.objects.get_or_create(
#         # tax_summary=TaxSummary.objects.get(year=tax_year),
#         opening_transaction=opening_transaction,
#         closing_transaction=closing_transaction,
#         revenue=revenue,
#         cost=cost,
#         profit_or_loss=profit_or_loss,
#         tax=tax_to_pay_from_transaction,
#     )