from django.db.models import F
from transactions.models import TaxSummary


def _update_tax_summary_equity(tax_year, revenue, cost, tax):
    if not TaxSummary.objects.filter(year=tax_year).exists():
        TaxSummary.objects.create(year=tax_year, revenue=0, cost=0, tax=0)

    print(f"ℹ️  Updated TaxSummary object with revenue: {revenue}, cost: {cost} and tax: {tax}")
    TaxSummary.objects.filter(year=tax_year).update(
        revenue=F("revenue") + revenue, cost=F("cost") + cost, tax=F("tax") + tax
    )
