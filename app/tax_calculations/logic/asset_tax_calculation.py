from transactions.models import AssetTransaction

from utils.choices import TransactionSide

def create_asset_tax_calculations(sell_transaction: AssetTransaction):
    print(sell_transaction)
    matching_buy_transactions = AssetTransaction.objects.filter(
        asset_name=sell_transaction.asset_name, side=TransactionSide.BUY.value, executed_at__lte=sell_transaction.executed_at
    ).order_by("executed_at")
    print(matching_buy_transactions)
    print(len(matching_buy_transactions))