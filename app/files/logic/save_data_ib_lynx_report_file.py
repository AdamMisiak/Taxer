import csv

def save_data_ib_lynx_report_file(file):
    # from transactions.logic import save_withholding_tax_transaction_object_ib_broker, save_trade_transaction_object, save_dividend_transaction_object, save_interest_rates_transaction_object

    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]
        print(row)
        # # NOTE transactions has to be chronogically!!!

        # # NOTE oddzielnie zysk z opcji i akcji i oddzielnie dywidendy
        # # INTEREST RATES
        # if row_type == "Interest" and row[1] == "Data" and "Investment Loan Interest for" in row[4]:
        #     save_interest_rates_transaction_object(row)

        # # TRANSACTION
        # if row_type == "Trades" and row[1] == "Data":
        #     _validate_row_ib_broker_file(row)
        #     save_trade_transaction_object(row)

        # # DIVIDEND
        # if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
        #     _validate_row_ib_broker_file(row)
        #     save_dividend_transaction_object(row)
        #     # save_dividend_object(row)

        # # WITHHOLDING TAX
        # elif row_type == "Withholding Tax" and row[1] == "Data" and not row[2].startswith("Total"):
        #     _validate_row_ib_broker_file(row)
        #     save_withholding_tax_transaction_object_ib_broker(row)