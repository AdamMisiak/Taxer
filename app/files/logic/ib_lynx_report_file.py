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

def save_data_ib_lynx_report_file(file):
    from transactions.logic2 import save_ib_lynx_transaction
    # from transactions.logic import save_withholding_tax_transaction_object_ib_broker, save_trade_transaction_object, save_dividend_transaction_object, save_interest_rates_transaction_object

    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]

        # # NOTE  add script to make transactions chronigically here

        # # NOTE oddzielnie zysk z opcji i akcji i oddzielnie dywidendy
        # INTEREST RATES
        if row_type == "Interest" and row[1] == "Data" and "Investment Loan Interest for" in row[4]:
            print(row)
            print("interest!!!")
            # save_interest_rates_transaction_object(row)

        # TRANSACTION
        if row_type == "Trades" and row[1] == "Data":
            _clean_up_row_ib_lynx_report_file(row)
            save_ib_lynx_transaction(row)

        # # DIVIDEND
        # if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
        #     _validate_row_ib_broker_file(row)
        #     save_dividend_transaction_object(row)
        #     # save_dividend_object(row)

        # # WITHHOLDING TAX
        # elif row_type == "Withholding Tax" and row[1] == "Data" and not row[2].startswith("Total"):
        #     _validate_row_ib_broker_file(row)
        #     save_withholding_tax_transaction_object_ib_broker(row)