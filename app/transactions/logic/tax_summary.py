from django.db.models import F
from transactions.models import TaxSummary

def _init_tax_summary(tax_year: int):
    if not TaxSummary.objects.filter(year=tax_year).exists():
        TaxSummary.objects.create(year=tax_year, revenue=0, cost=0, tax=0)

def _update_tax_summary(tax_year, revenue, cost, tax):
    _init_tax_summary(tax_year)

    print(f"ℹ️  Updated TaxSummary object with revenue: {revenue}, cost: {cost} and tax: {tax}")
    TaxSummary.objects.filter(year=tax_year).update(
        revenue=F("revenue") + revenue, cost=F("cost") + cost, tax=F("tax") + tax
    )