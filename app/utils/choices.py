from django.db import models

class AssetType(models.TextChoices):
    STOCKS = "Stocks", "Stocks"
    OPTIONS = "Options", "Options"
    DIVIDENDS = "Dividends", "Dividends"
    WITHHOLDING_TAX = "Withholding Tax", "Withholding Tax"
    OTHERS = "Others", "Others"

class TransactionSide(models.TextChoices):
    BUY = "Buy", "Buy"
    SELL = "Sell", "Sell"

class TransactionType(models.TextChoices):
    OPENING = "Opening", "Opening"
    CLOSING = "Closing", "Closing"

class Currency(models.TextChoices):
    USD = "USD", "USD"
    EUR = "EUR", "EUR"
    GBP = "GGP", "GBP"
    RUB = "RUB", "RUB"
    PLN = "PLN", "PLN"

class OptionType(models.TextChoices):
    CALL = "CALL", "CALL"
    PUT = "PUT", "PUT"

