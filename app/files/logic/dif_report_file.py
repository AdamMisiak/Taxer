from utils.choices import AssetType
from files.models import ReportFile
import csv


def save_data_dif_report_file(file, report_file_object: ReportFile):
    from transactions.logic2 import save_ib_lynx_asset_transaction, save_ib_lynx_dividend_transaction, save_ib_lynx_withholding_tax_transaction, save_ib_lynx_option_transaction, save_ib_lynx_interest_rate_transaction_object

    csvreader = csv.reader(file, delimiter=";")

    for row in csvreader:
        row_type = row[0]
        # # NOTE  add script to make transactions chronigically here
        print(row)
        # if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
        #     save_dividend_transaction_object(row)
        #     save_withholding_tax_object_dif_broker(row)
        
        # # INTEREST RATES
        # if row_type == "Interest" and row[1] == "Data" and "Investment Loan Interest for" in row[4]:
        #     save_ib_lynx_interest_rate_transaction_object(row, report_file_object)

        # # ASSETS
        # if row_type == "Trades" and row[1] == "Data" and row[3].startswith(AssetType.STOCKS.value):
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_asset_transaction(row, report_file_object)

        # # OPTIONS
        # if row_type == "Trades" and row[1] == "Data" and row[3] == "Equity and Index Options":
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_option_transaction(row, report_file_object)

        # # DIVIDENDS
        # if row_type == AssetType.DIVIDENDS.value and row[1] == "Data" and not row[2].startswith("Total"):
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_dividend_transaction(row, report_file_object)

        # # WITHHOLDING TAXES
        # elif row_type == AssetType.WITHHOLDING_TAX.value and row[1] == "Data" and not row[2].startswith("Total"):
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_withholding_tax_transaction(row, report_file_object)
