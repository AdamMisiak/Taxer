from transactions.models import DividendTransaction, WithholdingTaxTransaction
from datetime import timedelta
from utils.choices import TransactionSide


def create_dividend_tax_calculations(dividend_transaction: DividendTransaction):
    # from tax_calculations.logic import calculate_tax_single_transaction_same_quantity, calculate_tax_multiple_transactions

    withholding_tax_transaction = dividend_transaction.withholding_tax_transaction
    if withholding_tax_transaction:
        print(withholding_tax_transaction)

