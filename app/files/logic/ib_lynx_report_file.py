from utils.choices import AssetType, TransactionSide, Currency
from django.conf import settings
from files.models import ReportFile
from utils.models import Broker
import csv

def _clean_up_row_ib_lynx_report_file(row: list[str]):
    if row[5].startswith("U") and row[5][1:].isnumeric():
        del row[5]

    if row[3].startswith("Forex") and row[5].startswith("20") and len(row) == 16:
        row.insert(5, "")

    if row[3].startswith("U") and row[3][1:].isnumeric():
        del row[3]

    if row[2].startswith("U") and row[2][1:].isnumeric():
        del row[2]

def save_data_ib_lynx_report_file(file, report_file_object: ReportFile):
    from transactions.logic2 import save_ib_lynx_asset_transaction, save_ib_lynx_dividend_transaction, save_ib_lynx_withholding_tax_transaction
    # from transactions.logic import save_withholding_tax_transaction_object_ib_broker, save_trade_transaction_object, save_dividend_transaction_object, save_interest_rates_transaction_object

    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]

        # # NOTE  add script to make transactions chronigically here

        # # NOTE oddzielnie zysk z opcji i akcji i oddzielnie dywidendy
        # INTEREST RATES
        if row_type == "Interest" and row[1] == "Data" and "Investment Loan Interest for" in row[4]:
            print(row)
            # print("interest!!!")
            # save_interest_rates_transaction_object(row)

        # ASSETS
        if row_type == "Trades" and row[1] == "Data" and row[3] in [AssetType.STOCKS.value]:
            # print(row)
            _clean_up_row_ib_lynx_report_file(row)
            save_ib_lynx_asset_transaction(row, report_file_object)

        # DIVIDEND
        if row_type == AssetType.DIVIDENDS.value and row[1] == "Data" and not row[2].startswith("Total"):
            _clean_up_row_ib_lynx_report_file(row)
            save_ib_lynx_dividend_transaction(row, report_file_object)
            # _validate_row_ib_broker_file(row)
            # save_dividend_transaction_object(row)
            # save_dividend_object(row)

        # # WITHHOLDING TAX
        elif row_type == AssetType.WITHHOLDING_TAX.value and row[1] == "Data" and not row[2].startswith("Total"):
            _clean_up_row_ib_lynx_report_file(row)
            save_ib_lynx_withholding_tax_transaction(row, report_file_object)