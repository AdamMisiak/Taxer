from tax_summaries.models import DividendTaxSummary
from tax_calculations.models import DividendTaxCalculation

def _get_dividend_tax_summary(tax_year: int) -> DividendTaxSummary:
    dividend_tax_summary, _ = DividendTaxSummary.objects.get_or_create(
        year=tax_year,
        defaults={'revenue': 0, 'tax_paid': 0, 'tax': 0}
    )
    return dividend_tax_summary


def assign_dividend_tax_summary(tax_calculation: DividendTaxCalculation):
    dividend_tax_summary = _get_dividend_tax_summary(tax_calculation.dividend_transaction.executed_at.year)

    dividend_tax_summary.revenue += tax_calculation.revenue
    dividend_tax_summary.tax_paid += tax_calculation.cost
    dividend_tax_summary.tax += tax_calculation.tax
    dividend_tax_summary.save()

    tax_calculation.tax_summary = dividend_tax_summary
    tax_calculation.save()
