from transactions.models import OptionTransaction
from tax_calculations.models import OptionTaxCalculation
from datetime import timedelta
from django.conf import settings
from utils.choices import TransactionSide


def create_option_tax_calculations(closing_transaction: OptionTransaction):
    from tax_calculations.logic import calculate_tax_single_transaction_same_quantity_options

    # NOTE what if there is buy transaction with quantity 2 and sell with quantity 1 and then another with quant 1

    print(f"ℹ️  Search for matching transactions for the transactions: {closing_transaction}")
    opposite_side = TransactionSide.SELL.value if closing_transaction.side == TransactionSide.BUY.value else TransactionSide.BUY.value
    
    matching_opening_transactions = OptionTransaction.objects.filter(asset_name=closing_transaction.asset_name, side=opposite_side, strike_price=closing_transaction.strike_price, option_type=closing_transaction.option_type, executed_at__lte=closing_transaction.executed_at, as_closing_calculation__isnull=True, as_opening_calculation__isnull=True).order_by("executed_at")
    number_of_matching_opening_transactions = len(matching_opening_transactions)
    print(f"ℹ️  Found {number_of_matching_opening_transactions} matching transaction(s)")

    if number_of_matching_opening_transactions == 0:
        print("❌ No transactions found")
        return
    
    print(f"ℹ️  Found transaction(s): {matching_opening_transactions}\n")

    if number_of_matching_opening_transactions == 1:
        opening_transaction = matching_opening_transactions.first()
        print(f"ℹ️  Used {opening_transaction} transaction for the calculation")
        print(closing_transaction)
        print(opening_transaction)
        calculate_tax_single_transaction_same_quantity_options(opening_transaction, closing_transaction)

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