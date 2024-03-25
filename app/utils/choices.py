from django.db import models

class AssetType(models.TextChoices):
    STOCKS = "stocks", "Stocks"
    # TEST = "test", "Test"
    # SECOND_STEP = "secondStep", "Second step"

class TransactionSide(models.TextChoices):
    BUY = "buy", "Buy"
    SELL = "sell", "Sell"

class Currency(models.TextChoices):
    USD = "usd", "USD"
    EUR = "eur", "EUR"
    GBP = "gbp", "GBP"
    RUB = "rub", "RUB"


# NOTE add brokers like this aslo?