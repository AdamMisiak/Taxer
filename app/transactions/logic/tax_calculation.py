from django.conf import settings
from transactions.models import CurrencyRate, TaxCalculation, TaxSummary, Transaction


def _calculate_tax_option_sell(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    premium_pln = transaction_instance.value_pln
    tax_to_pay_from_transaction = round(premium_pln * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        tax_summary=TaxSummary.objects.get(year=tax_year),
        closing_transaction=transaction_instance,
        revenue=premium_pln,
        cost=0,
        profit_or_loss=premium_pln,
        tax=tax_to_pay_from_transaction,
    )


def _calculate_tax_option_buy(transaction_instance: Transaction):
    tax_year = transaction_instance.executed_at.year
    premium_pln = round(transaction_instance.value_pln, 2)
    tax_to_pay_from_transaction = round(premium_pln * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=transaction_instance,
        revenue=0,
        cost=premium_pln,
        profit_or_loss=-premium_pln,
        tax=-tax_to_pay_from_transaction,
    )


def calculate_tax_option(transaction_instance: Transaction):
    from transactions.logic import init_tax_summary

    init_tax_summary(transaction_instance.executed_at.year)
    print('OPTION calculate_tax_option')
    print(transaction_instance)

    if not transaction_instance.as_opening_calculation.all() and not transaction_instance.as_closing_calculation.all():
        # NOTE separated buy and sell bc when it was integrated sell was first and when creating tax instance, buy/expire was not there yet
        if transaction_instance.side == "Sell":
            _calculate_tax_option_sell(transaction_instance)
        elif transaction_instance.side == "Buy":
            _calculate_tax_option_buy(transaction_instance)
    else:
        print("⚠️  Option is already included in the tax calculations!")


def _calculate_tax_equity_same_quantity(opening_transaction: Transaction, closing_transaction: Transaction):
    tax_year = closing_transaction.executed_at.year or opening_transaction.year
    profit_or_loss = round(closing_transaction.value_pln - opening_transaction.value_pln, 2)
    tax_to_pay_from_transaction = round(profit_or_loss * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=closing_transaction.value_pln,
        cost=opening_transaction.value_pln,
        profit_or_loss=profit_or_loss,
        tax=tax_to_pay_from_transaction,
    )


# NOTE prowizje tez sie liczy do opcji https://www.youtube.com/watch?v=b3UQYeI7EYU


def _handle_one_transaction_use_case(opening_transaction: Transaction, closing_transaction: Transaction):
    if (
        opening_transaction.quantity == closing_transaction.quantity
        and not opening_transaction.as_opening_calculation.all()
    ):
        print(f"ℹ️  Used {opening_transaction} transaction for the calculation")
        print("ℹ️  One matching transaction use case")
        _calculate_tax_equity_same_quantity(opening_transaction, closing_transaction)
    else:
        print("⚠️  Haven't found any new matching transaction(s)!")


def _get_partial_quantity_for_transaction(closing_transaction_quantity, summary_opening_transaction_quantity):
    quantity_used_in_current_transaction = closing_transaction_quantity - summary_opening_transaction_quantity
    return quantity_used_in_current_transaction


def _calculate_tax_equity_partial_different_quantity(
    opening_transaction: Transaction, closing_transaction: Transaction, quantity: int = None
):
    # NOTE if quantity is None -> middle transaction -> ratio is 1 (no ratio) and revenue is 0 (only cost)
    # NOTE if quantity exists -> last partial transaction -> ratio is not 0 (used required %)

    ratio = quantity / opening_transaction.quantity if quantity else 1
    tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

    revenue = closing_transaction.value_pln if quantity else 0
    cost = round(opening_transaction.value_pln * ratio, 2)

    if quantity:
        profit_or_loss = round(revenue - cost, 2)
    else:
        profit_or_loss = round(-opening_transaction.value_pln, 2)
    tax = round(profit_or_loss * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax,
        quantity=quantity,
    )

# NOTE przekminic to
def _calculate_tax_equity_partial_different_quantity_temp2(
    opening_transaction: Transaction, closing_transaction: Transaction, quantity: int = None
):
    # NOTE needs to chekc if it is last transaction -> if closing trans quantity == summary open trans quantity
    # NOTE if it is not last -> do not include revenue

    ratio = quantity / opening_transaction.quantity if quantity else 1
    tax_year = closing_transaction.executed_at.year or opening_transaction.executed_at.year

    revenue = 0
    cost = round(opening_transaction.value_pln * ratio, 2)

    if quantity:
        profit_or_loss = round(revenue - cost, 2)
    else:
        profit_or_loss = round(-opening_transaction.value_pln, 2)
    tax = round(profit_or_loss * settings.TAX_RATE, 2)

    TaxCalculation.objects.create(
        tax_summary=TaxSummary.objects.get(year=tax_year),
        opening_transaction=opening_transaction,
        closing_transaction=closing_transaction,
        revenue=revenue,
        cost=cost,
        profit_or_loss=profit_or_loss,
        tax=tax,
        quantity=quantity,
    )


def _handle_few_transactions_equal_quantity_use_case(matching_transactions, closing_transaction):
    summary_opening_transaction_quantity = 0

    print(matching_transactions)
    for transaction in matching_transactions:
        # NOTE this can be calculated only for first found transaction with same quantity (FIFO rule)
        print(transaction.quantity)
        print(closing_transaction.quantity)
        print(transaction.as_opening_calculation.all())
        print(summary_opening_transaction_quantity)
        if (
            summary_opening_transaction_quantity == 0
            and transaction.quantity == closing_transaction.quantity
            and not transaction.as_opening_calculation.all()
            and not closing_transaction.as_opening_calculation.all()
        ):
            print(f"ℹ️  Used first transaction with matching quantity: {transaction}")
            _calculate_tax_equity_same_quantity(transaction, closing_transaction)
            break

        elif transaction.quantity <= closing_transaction.quantity and not transaction.as_opening_calculation.all():
            if summary_opening_transaction_quantity + transaction.quantity > closing_transaction.quantity:
                quantity = _get_partial_quantity_for_transaction(
                    closing_transaction.quantity, summary_opening_transaction_quantity
                )
                print(f"ℹ️  Used last partial transaction with {quantity} quantity: {transaction}")
                _calculate_tax_equity_partial_different_quantity(transaction, closing_transaction, quantity)
                break
            else:
                summary_opening_transaction_quantity += transaction.quantity
                print(f"ℹ️  Used middle transaction: {transaction}")
                _calculate_tax_equity_partial_different_quantity(transaction, closing_transaction)
        # NOTE use case when transaction has quantity from previosu calculation
        elif transaction.quantity <= closing_transaction.quantity and transaction.as_opening_calculation.all() and transaction.as_opening_calculation.last().quantity:
            print("3rd use case")
            print(transaction)
            print(closing_transaction)
            print(transaction.quantity)
            print(transaction.as_opening_calculation.last())
            print(transaction.as_opening_calculation.last().quantity)
    
            
            remaining_quantity = transaction.quantity - transaction.as_opening_calculation.last().quantity
            summary_opening_transaction_quantity += remaining_quantity
            print(f"ℹ️  Used partial transaction with {remaining_quantity} remaining quantity: {transaction}")
            _calculate_tax_equity_partial_different_quantity_temp2(transaction, closing_transaction, remaining_quantity)
        print("---------")

def calculate_tax_equity(transaction_instance: Transaction):
    from transactions.logic import init_tax_summary

    closing_transaction = transaction_instance
    init_tax_summary(closing_transaction.executed_at.year)

    print(f"ℹ️  Searching matching transactions for closing transaction: {closing_transaction}")

    matching_transactions = Transaction.objects.filter(
        asset_name=closing_transaction.asset_name, side="Buy", executed_at__lte=closing_transaction.executed_at
    ).order_by("executed_at")
    number_of_matching_transactions = len(matching_transactions)
    print(f"ℹ️  Found {number_of_matching_transactions} matching transaction(s)")
    print(f"ℹ️  Found transaction(s): {matching_transactions}\n")

    if number_of_matching_transactions == 1:
        _handle_one_transaction_use_case(
            opening_transaction=matching_transactions[0], closing_transaction=closing_transaction
        )

    elif number_of_matching_transactions > 1:
        # NOTE sprawdzic dla TSLA czy pokrywa sie z google sheet (kolejnosc, daty, ceny itp)
        # NOTE if save transaction 2 times, it's going to calculate tax 2 times
        _handle_few_transactions_equal_quantity_use_case(
            matching_transactions=matching_transactions, closing_transaction=closing_transaction
        )

    else:
        print(f"🛑 Haven't found matching transaction(s) for {closing_transaction}")

    # NOTE some logic to raise exception when calculation failed
    # if matching_transaction_found:
    #     _calculate_tax_equity(opening_transaction, closing_transaction)
    # else:
    #     raise Exception(f"🛑 Wasn't able to calculate tax for {closing_transaction}")

# NOTE tax summary dodac podzial na tax z danej kategorii, div, options etc

def calculate_tax_dividend(transaction_instance: Transaction):
    from transactions.logic import init_tax_summary

    withholding_tax_instance = transaction_instance.withholding_tax
    # print(transaction_instance)
    # print(withholding_tax_instance)
    if withholding_tax_instance:
        tax_year = transaction_instance.executed_at.year

        dividend_pln = round(transaction_instance.value_pln, 2)
        withholding_tax_pln = round(withholding_tax_instance.value_pln, 2)
        profit_or_loss = round(dividend_pln - withholding_tax_pln, 2)
        tax_to_pay_from_dividend = round((dividend_pln * settings.TAX_RATE) - withholding_tax_pln, 2)

        init_tax_summary(tax_year)

        TaxCalculation.objects.create(
            tax_summary=TaxSummary.objects.get(year=tax_year),
            opening_transaction=withholding_tax_instance,
            closing_transaction=transaction_instance,
            revenue=dividend_pln,
            cost=withholding_tax_pln,
            profit_or_loss=profit_or_loss,
            tax=tax_to_pay_from_dividend,
        )

# TODO opening_transaction has to be transaction model
# TODO create transaction main model -> option transaction, Stocks transaction, dividend etc as children
# TODO change signals to celery task?
# TODO tax calculation should be also separated to each category
# TODO separated apps for trasnactions,taxes etc?