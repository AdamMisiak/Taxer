from rates.models import CurrencyRate
from datetime import datetime, timedelta
from utils.exceptions import QueryException

def get_previous_day_curreny_rate(date: datetime):
    if CurrencyRate.objects.filter(date__lt=date).exists():
        return CurrencyRate.objects.filter(date__lt=date).order_by("-date").first()
    else:
        raise QueryException(f"❌ Currency rate for '{date}' is not available!")
