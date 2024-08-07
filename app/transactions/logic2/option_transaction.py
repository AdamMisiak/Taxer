from datetime import datetime, timedelta
from files.models import ReportFile
from utils.logic import get_previous_day_curreny_rate
from transactions.models import OptionTransaction
from utils.choices import TransactionSide, Currency, OptionType, TransactionType

def _get_type(tags: str) -> str:
    # NOTE is it always C OR O??? Maybe there are some edge cases
    if "C" in tags:
        return TransactionType.CLOSING.value
    elif "O" in tags:
        return TransactionType.OPENING.value
    else:
        raise Exception(f"{tags} can not be handled!!")
    # return TransactionType.CLOSING.value if "C" in tags else TransactionType.OPENING.value

def _get_base_instrument(option_name: str) -> str:
    # NOTE Change with REGEX?
    return option_name.split(" ")[0]

def _get_option_type(option_name: str) -> str:
    # NOTE Change with REGEX?
    return OptionType.CALL.value if option_name[-1] == "C" else OptionType.PUT.value

def _get_strike_price(option_name: str) -> float:
    # NOTE Change with REGEX?
    return float(option_name.split()[-2])

def _get_expiration_date(option_name: str) -> float:
    # NOTE Change with REGEX?
    return datetime.strptime(option_name.split()[1], "%d%b%y")

def save_ib_lynx_option_transaction(row: list[str], report_file_object: ReportFile):
    asset_name_index = 5
    asset_type_index = 3
    price_index = 8
    quantity_index = 7
    value_index = 10
    currency_index = 4
    fee_index = 11
    executed_at_index = 6
    tags_index = -1

    executed_at = datetime.strptime(row[executed_at_index], "%Y-%m-%d, %H:%M:%S") + timedelta(hours=6)
    previous_day_currency_rate = get_previous_day_curreny_rate(executed_at)

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
    side = TransactionSide.BUY.value if quantity_raw > 0 else TransactionSide.SELL.value
    currency = getattr(Currency, row[currency_index]).value

    price = round(float(row[price_index]), 2)
    fee = abs(float(row[fee_index]))
    quantity = abs(quantity_raw)
    expired = price == 0.0 and row[tags_index] in ["A;C", "C;Ep"]

    value = round(abs(float(row[value_index])), 2)
    full_value = round(value + fee, 2) if side == "Buy" else round(value - fee, 2)

    value_pln = (
        round(value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else value
    )
    full_value_pln = (
        round(full_value * getattr(previous_day_currency_rate, currency.lower()), 2) if currency.lower() != "pln" else full_value
    )

    OptionTransaction.objects.get_or_create(
        asset_name=asset_name,
        side=side,
        type=_get_type(row[tags_index]),
        price=price,
        quantity=quantity,
        base_instrument=_get_base_instrument(asset_name),
        option_type=_get_option_type(asset_name),
        strike_price=_get_strike_price(asset_name),
        expiration_date=_get_expiration_date(asset_name),
        expired=expired,
        executed_at=executed_at,
        raw_data=str(row),
        defaults={
            "report_file": report_file_object,
            "previous_day_currency_rate": previous_day_currency_rate,
            "asset_type": asset_type,
            "currency": currency,
            "fee": fee,
            "value": value,
            "full_value": full_value,
            "value_pln": value_pln,
            "full_value_pln": full_value_pln,
        },
    )
