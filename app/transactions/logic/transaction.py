import csv
from datetime import datetime, timedelta

from transactions.models import CurrencyRate, Transaction, Dividend, WithholdingTax


def _get_option_type(option_name: str) -> str:
    return "CALL" if option_name[-1] == "C" else "PUT"


def _get_strike_price(option_name: str) -> float:
    return float(option_name.split()[-2])


def _validate_row_ib_broker_file(row):
    if row[5].startswith("U") and row[5][1:].isnumeric():
        del row[5]

    if row[3].startswith("Forex") and row[5].startswith("20") and len(row) == 16:
        row.insert(5, "")


def _save_transaction_object(row: list[str]):
    asset_name_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d, %H:%M:%S") + timedelta(hours=6)
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=executed_at).order_by("-date").first()

    asset_name = row[asset_name_index]
    asset_type = (
        row[asset_type_index]
        .replace(
            " - Held with Interactive Brokers (U.K.) Limited carried by Interactive Brokers LLC",
            "",
        )
        .strip()
    )
    # Creating raw quantity (negative or positive) to determine side of the transaction
    quantity_raw = float(row[quantity_index].replace(",", ""))
    side = "Buy" if quantity_raw > 0 else "Sell"
    quantity = abs(quantity_raw)
    currency = row[currency_index]
    # NOTE Watch of for forex records
    price = round(float(row[price_index]), 2)
    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )
    fee = abs(float(row[fee_index]))
    is_option = asset_type == "Equity and Index Options"

    Transaction.objects.get_or_create(
        asset_name=asset_name,
        side=side,
        price=price,
        quantity=quantity,
        executed_at=executed_at,
        defaults={
            "asset_type": asset_type,
            "value": value,
            "value_pln": value_pln,
            "currency": currency,
            "previous_day_currency_rate": previous_day_currency_rate,
            "fee": fee,
            "option_type": _get_option_type(asset_name) if is_option else "",
            "strike_price": _get_strike_price(asset_name) if is_option else None,
        },
    )

# NOTE move it to dividend file
def _save_dividend_object(row: list[str]):
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    received_at_index = 3

    received_at = datetime.strptime(row[received_at_index], "%Y-%m-%d")
    # NOTE double check if for divs I should also take previous day currency rate!
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=received_at).order_by("-date").first()

    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    # NOTE czy jest mozliwe miec takie same obiekty? przyklad ENB
    Dividend.objects.get_or_create(
        asset_name=asset_name,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        received_at=received_at,
    )

# NOTE move it to withoolding tax file
def _save_withholding_tax_object(row: list[str]):
    print(row)
    asset_name_index = 4
    value_index = 5
    currency_index = 2
    paid_at_index = 3


    paid_at = datetime.strptime(row[paid_at_index], "%Y-%m-%d")
    previous_day_currency_rate = CurrencyRate.objects.filter(date__lt=paid_at).order_by("-date").first()

    asset_name = row[asset_name_index].split("(")[0].strip()
    currency = row[currency_index]
    value = round(abs(float(row[value_index])), 2)
    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )

    print(asset_name)
    print(currency)
    print(previous_day_currency_rate)
    print(paid_at)
    # NOTE check what happen when more than one record here
    matching_dividend_object = Dividend.objects.filter(
        asset_name=asset_name,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        received_at=paid_at,
    ).first()
    

    withholding_tax_object = WithholdingTax.objects.create(
        asset_name=asset_name,
        value=value,
        value_pln=value_pln,
        currency=currency,
        previous_day_currency_rate=previous_day_currency_rate,
        paid_at=paid_at,
    )

    matching_dividend_object.withholding_tax = withholding_tax_object
    matching_dividend_object.save()


# NOTE should this file be here? it is related not only to transaciton
def save_data_ib_broker_file(file):
    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]
        # NOTE transactions has to be chronogically!!!

        # TRANSACTION
        if row_type == "Trades" and row[1] == "Data":
            _validate_row_ib_broker_file(row)
            _save_transaction_object(row)

        # DIVIDEND
        elif row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
            _save_dividend_object(row)

        # WITHHOLDING TAX
        elif row_type == "Withholding Tax" and row[1] == "Data" and not row[2].startswith("Total"):
            _save_withholding_tax_object(row)


def save_data_dif_broker_file(file):
    csvreader = csv.reader(file, delimiter=";")

    for row in csvreader:
        row_type = row[0]

        # DIVIDEND
        if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
            _save_dividend_object(row)

        # WITHHOLDING TAX
        elif row_type == "Withholding Tax" and row[1] == "Data":
            pass
            # _save_dividend_object(row)

            # NOTE ENB	10.2	43.5	USD	-	June 1, 2022 double check why 3 times saved this record