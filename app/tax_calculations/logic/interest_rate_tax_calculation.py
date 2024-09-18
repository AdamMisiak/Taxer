from transactions.models import InterestRateTransaction
from tax_calculations.models import InterestRateTaxCalculation
from django.conf import settings


def create_interest_rate_tax_calculations(interest_rate_transaction: InterestRateTransaction):
    tax_year = interest_rate_transaction.executed_at.year
    interests_rate_pln = round(interest_rate_transaction.value_pln, 2)
    tax_to_pay_from_transaction = round(interests_rate_pln * settings.TAX_RATE, 2)

    InterestRateTaxCalculation.objects.create(
        # tax_summary=TaxSummary.objects.get(year=tax_year),
        interest_rate_transaction=interest_rate_transaction,
        revenue=0,
        cost=interests_rate_pln,
        profit_or_loss=-interests_rate_pln,
        tax=-tax_to_pay_from_transaction,
    )
