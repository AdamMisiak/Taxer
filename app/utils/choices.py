from django.db import models

class AssetType(models.TextChoices):
    STOCKS = "Stocks", "Stocks"
    # DIVIDENDS = "Dividends", "Dividends"
    # TEST = "test", "Test"
    # SECOND_STEP = "secondStep", "Second step"

class TransactionSide(models.TextChoices):
    BUY = "Buy", "Buy"
    SELL = "Sell", "Sell"

class Currency(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    GBP = "GGP", "GBP"
    RUB = "RUB", "RUB"


# NOTE add brokers like this aslo?