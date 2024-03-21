import csv
import re
from datetime import datetime

from rates.models import CurrencyRate


def save_data_currency_rate_file(file):
    csvreader = csv.reader(file, delimiter=";")

    for row in csvreader:
        if len(row) == 0 or not re.match(r"^([\d]+)$", row[0]):
            continue

        CurrencyRate.objects.get_or_create(
            date=datetime.strptime(row[0], "%Y%m%d"),
            defaults={
                "usd": float(row[2].replace(",", ".")),
                "eur": float(row[8].replace(",", ".")),
                "gbp": float(row[11].replace(",", ".")),
                "chf": float(row[10].replace(",", ".")),
                "rub": float(row[30].replace(",", ".")) if row[30] else None,
            },
        )
