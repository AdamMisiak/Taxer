from utils.choices import AssetType
from files.models import ReportFile
import csv


def save_data_dif_report_file(file, report_file_object: ReportFile):
    from transactions.logic2 import save_dif_asset_transaction

    csvreader = csv.reader(file, delimiter=";")

    for row in csvreader:
        # # NOTE  add script to make transactions chronigically here
        # if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
        #     save_dividend_transaction_object(row)
        #     save_withholding_tax_object_dif_broker(row)
        
        # ASSETS
        if row[4] in ["Bought", "Sold"] and len(row[2]) <= 5:
            save_dif_asset_transaction(row, report_file_object)

        # # DIVIDENDS
        # if row_type == AssetType.DIVIDENDS.value and row[1] == "Data" and not row[2].startswith("Total"):
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_dividend_transaction(row, report_file_object)

        # # WITHHOLDING TAXES
        # elif row_type == AssetType.WITHHOLDING_TAX.value and row[1] == "Data" and not row[2].startswith("Total"):
        #     _clean_up_row_ib_lynx_report_file(row)
        #     save_ib_lynx_withholding_tax_transaction(row, report_file_object)
