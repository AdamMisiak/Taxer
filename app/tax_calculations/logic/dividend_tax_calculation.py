from transactions.models import DividendTransaction, WithholdingTaxTransaction
from datetime import timedelta
from utils.choices import TransactionSide


def create_dividend_tax_calculations(dividend_transaction: DividendTransaction):
    from tax_calculations.logic import calculate_tax_single_transaction_same_quantity, calculate_tax_multiple_transactions

    # NOTE no need to search for the matching WH transactions
    
    
    # number_of_matching_buy_transactions = len(matching_buy_transactions)
    # print(f"ℹ️  Found {number_of_matching_buy_transactions} matching transaction(s)")

    # if number_of_matching_buy_transactions == 0:
    #     print("❌ No transactions found.")
    #     return
    
    # print(f"ℹ️  Found transaction(s): {matching_buy_transactions}\n")


    # if number_of_matching_buy_transactions == 1:
    #     buy_transaction = matching_buy_transactions.first()
    #     if buy_transaction.quantity == sell_transaction.quantity and not buy_transaction.as_opening_calculation.all():
    #         print(f"ℹ️  Used {buy_transaction} transaction for the calculation")
    #         print("ℹ️  One matching transaction use case")
    #         calculate_tax_single_transaction_same_quantity(
    #             opening_transaction=buy_transaction, closing_transaction=sell_transaction
    #         )

    # elif number_of_matching_buy_transactions > 1:
    #     calculate_tax_multiple_transactions(
    #         matching_opening_transactions=matching_buy_transactions, closing_transaction=sell_transaction
    #     )