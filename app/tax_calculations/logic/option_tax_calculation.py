from transactions.models import OptionTransaction
from tax_calculations.models import OptionTaxCalculation
from datetime import timedelta
from django.conf import settings
from utils.choices import TransactionSide


def create_option_tax_calculations(closing_transaction: OptionTransaction):
    from tax_calculations.logic import calculate_tax_single_transaction_same_quantity_options, calculate_tax_multiple_transactions

    # NOTE what if there is buy transaction with quantity 2 and sell with quantity 1 and then another with quant 1

    print(f"ℹ️  Search for matching transactions for the transaction: {closing_transaction}")
    opposite_side = TransactionSide.SELL.value if closing_transaction.side == TransactionSide.BUY.value else TransactionSide.BUY.value
    
    matching_opening_transactions = OptionTransaction.objects.filter(
        base_instrument=closing_transaction.base_instrument,
        expiration_date=closing_transaction.expiration_date,
        strike_price=closing_transaction.strike_price,
        option_type=closing_transaction.option_type,
        side=opposite_side,
        closing=False,
        executed_at__lte=closing_transaction.executed_at,
        as_closing_calculation__isnull=True,
        as_opening_calculation__isnull=True
    ).order_by("executed_at")
    if not matching_opening_transactions:
        print('SECOND SEARCH')
        matching_opening_transactions = OptionTransaction.objects.filter(
            base_instrument=closing_transaction.base_instrument,
            expiration_date=closing_transaction.expiration_date,
            strike_price=closing_transaction.strike_price,
            option_type=closing_transaction.option_type,
            side=opposite_side,
            closing=False,
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
        # print(f"ℹ️  Used {opening_transaction} transaction for the calculation")
        # print(closing_transaction)
        # print(opening_transaction)
        # NOTE additional check here - if quantities are equal? 
        if opening_transaction.quantity == closing_transaction.quantity:
            calculate_tax_single_transaction_same_quantity_options(opening_transaction, closing_transaction)
        else:
            print(opening_transaction.id)
            print(opening_transaction)
            print(closing_transaction.id)
            print(closing_transaction)
            ratio = closing_transaction.quantity / opening_transaction.quantity
            print(ratio)

            # tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year
            revenue = opening_transaction.full_value_pln*ratio
            profit_or_loss = round(revenue - closing_transaction.full_value_pln, 2)
            tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

            OptionTaxCalculation.objects.get_or_create(
                # tax_summary=TaxSummary.objects.get(year=tax_year),
                opening_transaction=opening_transaction,
                closing_transaction=closing_transaction,
                revenue=revenue,
                cost=closing_transaction.full_value_pln,
                profit_or_loss=profit_or_loss,
                tax=tax_to_pay_from_transaction,
                quantity=closing_transaction.quantity,
            )
            print("-------Some other handling function here-------")
            # NOTE: similar to calculate_tax_multiple_transactions? Or cover only oen use case for now? when two closing transaction are equal
            # or add this new use case to calculate_tax_multiple_transactions?
    


    # NOTE why it is still shwoing only 1 transaction opening to MPW 24MAR23 - it is taking one BUY (1.0 out of 2.0) transaction as closing one and finding opening one as SELL (2.0)
    # NOTE partial transactions for AMT are wrong - check that!!
    # MPW 24MAR23 also not working -> quantity not icnluded -> connected 1.0 BUY with 2.0 SELL
    # MPW 28JUL23 same probably
    # check rest of lonely transactions (which are not at the end of the year)

    # after this -> check if this query above is working fine with expiration_date condition



    elif number_of_matching_opening_transactions > 1:
        calculate_tax_multiple_transactions(
            model=OptionTaxCalculation, matching_opening_transactions=matching_opening_transactions, closing_transaction=closing_transaction
        )
    print('--------')



    # withholding_tax_transaction = dividend_transaction.withholding_tax_transaction
    # if withholding_tax_transaction:

    #     tax_year = dividend_transaction.executed_at.year
    #     asset_name = dividend_transaction.asset_name

    #     dividend_pln = round(dividend_transaction.value_pln, 2)
    #     withholding_tax_pln = round(withholding_tax_transaction.value_pln, 2)
    #     dividend_net = round(dividend_pln - withholding_tax_pln, 2)

    #     tax_rate = settings.CUSTOM_DIVIDEND_RATES.get(asset_name, settings.TAX_RATE)
    #     tax_to_pay_from_dividend = round((dividend_pln * tax_rate) - withholding_tax_pln, 2)

    #     # init_tax_summary(tax_year)

    #     DividendTaxCalculation.objects.create(
    #         # tax_summary=TaxSummary.objects.get(year=tax_year),
    #         withholding_tax_transaction=withholding_tax_transaction,
    #         dividend_transaction=dividend_transaction,
    #         revenue=dividend_pln,
    #         cost=withholding_tax_pln,
    #         profit_or_loss=dividend_net,
    #         tax=tax_to_pay_from_dividend,
    #         tax_rate=tax_rate,
    #     )
    # else:
    #     print(f"❌ Withholding tax transaction is missing for {dividend_transaction}")