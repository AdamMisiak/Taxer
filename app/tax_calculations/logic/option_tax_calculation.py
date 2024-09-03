from transactions.models import OptionTransaction
from tax_calculations.models import OptionTaxCalculation
from django.conf import settings
from utils.choices import TransactionSide, TransactionType


# TODO REFACTOR THIS FOR SURE!!
def create_option_tax_calculations(closing_transaction: OptionTransaction):
    from tax_calculations.logic import calculate_tax_for_complete_transaction, calculate_tax_multiple_transactions

    print(f"ℹ️  Search for matching transactions for the transaction: {closing_transaction}")
    opposite_side = TransactionSide.SELL.value if closing_transaction.side == TransactionSide.BUY.value else TransactionSide.BUY.value
    
    matching_opening_transactions = OptionTransaction.objects.filter(
        base_instrument=closing_transaction.base_instrument,
        expiration_date=closing_transaction.expiration_date,
        strike_price=closing_transaction.strike_price,
        option_type=closing_transaction.option_type,
        side=opposite_side,
        type=TransactionType.OPENING.value,
        executed_at__lte=closing_transaction.executed_at,
        as_closing_calculation__isnull=True,
        as_opening_calculation__isnull=True
    ).order_by("executed_at")
    if not matching_opening_transactions:
        print("ℹ️  Search for matching transactions with quantity for the same transaction")
        matching_opening_transactions = OptionTransaction.objects.filter(
            base_instrument=closing_transaction.base_instrument,
            expiration_date=closing_transaction.expiration_date,
            strike_price=closing_transaction.strike_price,
            option_type=closing_transaction.option_type,
            side=opposite_side,
            type=TransactionType.OPENING.value,
            executed_at__lte=closing_transaction.executed_at,
            # as_closing_calculation__quantity__isnull=True,
            as_opening_calculation__quantity__isnull=False
        ).order_by("executed_at")
    number_of_matching_opening_transactions = len(matching_opening_transactions)
    print(f"ℹ️  Found {number_of_matching_opening_transactions} matching transaction(s)")

    if number_of_matching_opening_transactions == 0:
        print("❌ No transactions found")
        return
    
    print(f"ℹ️  Found transaction(s): {matching_opening_transactions}\n")

    if number_of_matching_opening_transactions == 1:
        opening_transaction = matching_opening_transactions.first()
        if opening_transaction.quantity == closing_transaction.quantity:
            print(f"ℹ️  Used {opening_transaction} transaction for the calculation")
            calculate_tax_for_complete_transaction(OptionTaxCalculation, opening_transaction, closing_transaction)
        else:
            ratio = closing_transaction.quantity / opening_transaction.quantity
            print(f"ℹ️  Used {opening_transaction} transaction with {ratio} ratio for the calculation")
            # calculate_tax_single_transaction_different_quantity_options(opening_transaction, closing_transaction, ratio)

            # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year
            opening_is_sell = opening_transaction.type == TransactionType.OPENING and opening_transaction.side == TransactionSide.SELL
            opening_is_buy = opening_transaction.type == TransactionType.OPENING and opening_transaction.side == TransactionSide.BUY
            



            if opening_is_sell:
                revenue = opening_transaction.full_value_pln*ratio
                cost = closing_transaction.full_value_pln
                profit_or_loss = round(revenue - cost, 2)
            elif opening_is_buy:
                revenue = closing_transaction.full_value_pln*ratio
                cost = opening_transaction.full_value_pln
                profit_or_loss = round(revenue - cost, 2)




            tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)


            OptionTaxCalculation.objects.get_or_create(
                # tax_summary=TaxSummary.objects.get(year=tax_year),
                opening_transaction=opening_transaction,
                closing_transaction=closing_transaction,
                revenue=revenue,
                cost=cost,
                profit_or_loss=profit_or_loss,
                tax=tax_to_pay_from_transaction,
                quantity=closing_transaction.quantity,
            )
            # NOTE refactor + split this function into smaller ones -> same as calculate_tax_multiple_transactions for assets







    # NOTE "calculate_tax_multiple_transactions_same_quantity" was used for options - doing wrong calculations
    # has to write new `calculate_tax_multiple_transactions` for options only 
    # rememmber about the split (as above using opening_is_sell var) when opening is sell or buy 
    # Example: tax calculations for AMT 15SEP23

    # NOTE 2 check if those two if + elif are not failing + check how it works overall
    # similar idea to the previous optons calculations split


    




    # NOTE partial transactions for AMT are wrong - check that!!
    # AMT 15SEP23 - nie mozna uzyc funkcji z assets bo w options jest odwrotnie -> sell to jest opening trans
    # revenue w calculate_tax_multiple_transactions_same_quantity nie powinno byc 0


    # NOTE add closing and opening field to assets + options models (buy and sell does not mean tha transaction was opened/closed)

    # MPW 24MAR23 also not working -> quantity not icnluded -> connected 1.0 BUY with 2.0 SELL
    # MPW 28JUL23 same probably

    # after this -> check if this query above is working fine with expiration_date condition

    elif number_of_matching_opening_transactions > 1:
        calculate_tax_multiple_transactions(
            model=OptionTaxCalculation, matching_opening_transactions=matching_opening_transactions, closing_transaction=closing_transaction
        )
