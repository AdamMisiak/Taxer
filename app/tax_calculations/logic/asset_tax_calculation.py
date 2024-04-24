from transactions.models import AssetTransaction

from utils.choices import TransactionSide

def create_asset_tax_calculations(sell_transaction: AssetTransaction):
    print(f"ℹ️  Searching matching transactions for closing transaction: {sell_transaction}")
    matching_buy_transactions = AssetTransaction.objects.filter(
        asset_name=sell_transaction.asset_name, side=TransactionSide.BUY.value, executed_at__lte=sell_transaction.executed_at
    ).order_by("executed_at")
    number_of_matching_buy_transactions = len(matching_buy_transactions)
    print(f"ℹ️  Found {number_of_matching_buy_transactions} matching transaction(s)")
    print(f"ℹ️  Found transaction(s): {matching_buy_transactions}\n")


    if number_of_matching_buy_transactions == 1:
        buy_transaction = matching_buy_transactions.first()
        if buy_transaction.quantity == sell_transaction.quantity and not buy_transaction.as_opening_calculation.all():
            print('I IS A MATCH!')
        # _handle_one_transaction_use_case(
        #     opening_transaction=matching_transactions[0], closing_transaction=closing_transaction
        # )