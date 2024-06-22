from transactions.models import AssetTransaction
from tax_calculations.models import AssetTaxCalculation
from datetime import timedelta
from utils.choices import TransactionSide


def create_asset_tax_calculations(sell_transaction: AssetTransaction):
    from tax_calculations.logic import calculate_tax_single_transaction_same_quantity, calculate_tax_multiple_transactions

    print(f"ℹ️  Search for matching transactions for the closing transactions: {sell_transaction}")
    # NOTE "+ timedelta(days=3)" because some transactions are book on Monday next week -> there is first sell and but after that
    matching_buy_transactions = AssetTransaction.objects.filter(
        asset_name=sell_transaction.asset_name, side=TransactionSide.BUY.value, executed_at__lte=sell_transaction.executed_at + timedelta(days=3) 
    ).order_by("executed_at")
    number_of_matching_buy_transactions = len(matching_buy_transactions)
    print(f"ℹ️  Found {number_of_matching_buy_transactions} matching transaction(s)")

    if number_of_matching_buy_transactions == 0:
        print("❌ No transactions found")
        return
    
    print(f"ℹ️  Found transaction(s): {matching_buy_transactions}\n")


    if number_of_matching_buy_transactions == 1:
        buy_transaction = matching_buy_transactions.first()
        if buy_transaction.quantity == sell_transaction.quantity and not buy_transaction.as_opening_calculation.all():
            print(f"ℹ️  Used {buy_transaction} transaction for the calculation")
            print("ℹ️  One matching transaction use case")
            calculate_tax_single_transaction_same_quantity(
                opening_transaction=buy_transaction, closing_transaction=sell_transaction
            )

    elif number_of_matching_buy_transactions > 1:
        calculate_tax_multiple_transactions(
            model=AssetTaxCalculation, matching_opening_transactions=matching_buy_transactions, closing_transaction=sell_transaction
        )