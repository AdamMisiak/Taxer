from django.db import models

class AssetType(models.TextChoices):
    STOCKS = "stocks", "Stocks"
    # TEST = "test", "Test"
    # SECOND_STEP = "secondStep", "Second step"

class TransactionSide(models.TextChoices):
    BUY = "buy", "Buy"
