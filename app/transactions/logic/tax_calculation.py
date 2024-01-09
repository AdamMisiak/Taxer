from django.conf import settings
from transactions.models import CurrencyRate, TaxCalculation, Transaction


def calculate_tax_dividend(transaction_instance: Transaction):
    pass

def _calculate_tax_option_sell(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    premium_pln = transaction_instance.value_pln
    tax_to_pay_from_transaction = round(premium_pln * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        closing_transaction=transaction_instance,
        revenue=premium_pln,
        cost=0,
        profit_or_loss=premium_pln,
        tax=tax_to_pay_from_transaction,
    )

    # _update_tax_summary_equity(
    #     tax_year=tax_year,
    #     revenue=closing_transaction.value_pln,
    #     cost=opening_transaction.value_pln,
    #     tax=tax_to_pay_from_transaction,
    # )

def _calculate_tax_option_buy(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    premium_pln = transaction_instance.value_pln
    tax_to_pay_from_transaction = round(premium_pln * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        opening_transaction=transaction_instance,
        revenue=0,
        cost=premium_pln,
        profit_or_loss=-premium_pln,
        tax=-tax_to_pay_from_transaction,
    )

    # _update_tax_summary_equity(
    #     tax_year=tax_year,
    #     revenue=closing_transaction.value_pln,
    #     cost=opening_transaction.value_pln,
    #     tax=tax_to_pay_from_transaction,
    # )

def calculate_tax_option(transaction_instance: Transaction):
    from transactions.logic import _update_tax_summary_equity

    if not transaction_instance.as_opening_calculation.all() and not transaction_instance.as_closing_calculation.all():
        if transaction_instance.side == "Sell":
            _calculate_tax_option_sell(transaction_instance)
        # NOTE check if price is not 0? = expired OR new field for transcation
        elif transaction_instance.side == "Buy":
            _calculate_tax_option_buy(transaction_instance)
    else:
        print("⚠️  Option is already included in the tax calculations!")
        
    # update_tax_object(tax_year, tax_to_pay_from_transaction)



def _calculate_tax_equity_one_transaction(opening_transaction: Transaction, closing_transaction: Transaction):
    from transactions.logic import _update_tax_summary_equity

    tax_year = closing_transaction.executed_at.year
    profit_or_loss = round(closing_transaction.value_pln - opening_transaction.value_pln, 2)
    tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=closing_transaction.value_pln,
        cost=opening_transaction.value_pln,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay_from_transaction,
    )
    _update_tax_summary_equity(
        tax_year=tax_year,
        revenue=closing_transaction.value_pln,
        cost=opening_transaction.value_pln,
        tax=tax_to_pay_from_transaction,
    )


def calculate_tax_equity(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    closing_transaction = transaction_instance

    matching_transactions = Transaction.objects.filter(asset_name=closing_transaction.asset_name, side="Buy").order_by(
        "executed_at"
    )
    number_of_matching_transactions = len(matching_transactions)
    print(f"ℹ️  Found {number_of_matching_transactions} matching transaction(s)")
    if number_of_matching_transactions == 1:
        opening_transaction = matching_transactions[0]
        if (
            opening_transaction.quantity == closing_transaction.quantity
            and not opening_transaction.as_opening_calculation.all()
        ):
            _calculate_tax_equity_one_transaction(opening_transaction, closing_transaction)
        else:
            print("⚠️  Haven't found any new matching transaction(s)!")

    elif number_of_matching_transactions > 1:
        pass

    else:
        print(f"🛑 Haven't found matching transaction(s) for {closing_transaction}")
