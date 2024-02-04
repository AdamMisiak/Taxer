import csv


def _validate_row_ib_broker_file(row):
    if row[5].startswith("U") and row[5][1:].isnumeric():
        del row[5]

    if row[3].startswith("Forex") and row[5].startswith("20") and len(row) == 16:
        row.insert(5, "")

    if row[3].startswith("U") and row[3][1:].isnumeric():
        del row[3]

    if row[2].startswith("U") and row[2][1:].isnumeric():
        del row[2]

def save_data_ib_broker_file(file):
    from transactions.logic import save_withholding_tax_transaction_object_ib_broker, save_trade_transaction_object, save_dividend_transaction_object

    csvreader = csv.reader(file)

    for row in csvreader:
        row_type = row[0]
        # NOTE transactions has to be chronogically!!!

        # TRANSACTION
        if row_type == "Trades" and row[1] == "Data":
            print(row)
            _validate_row_ib_broker_file(row)
            save_trade_transaction_object(row)

        # DIVIDEND
        if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
            _validate_row_ib_broker_file(row)
            save_dividend_transaction_object(row)
            # save_dividend_object(row)

        # WITHHOLDING TAX
        elif row_type == "Withholding Tax" and row[1] == "Data" and not row[2].startswith("Total"):
            _validate_row_ib_broker_file(row)
            save_withholding_tax_transaction_object_ib_broker(row)


def save_data_dif_broker_file(file):
    from transactions.logic import save_dividend_object, save_withholding_tax_object_dif_broker

    csvreader = csv.reader(file, delimiter=";")

    for row in csvreader:
        row_type = row[0]

        # DIVIDEND
        if row_type == "Dividends" and row[1] == "Data" and not row[2].startswith("Total"):
            save_dividend_object(row)
            save_withholding_tax_object_dif_broker(row)
