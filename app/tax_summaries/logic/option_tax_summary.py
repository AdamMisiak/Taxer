from tax_summaries.models import OptionTaxSummary
from tax_calculations.models import OptionTaxCalculation

def _get_option_tax_summary(tax_year: int) -> OptionTaxSummary:
    option_tax_summary, _ = OptionTaxSummary.objects.get_or_create(
        year=tax_year,
        defaults={'revenue': 0, 'cost': 0, "profit_or_loss": 0, 'tax': 0}
    )
    return option_tax_summary


def assign_option_tax_summary(tax_calculation: OptionTaxCalculation):
    option_tax_summary = _get_option_tax_summary(tax_calculation.closing_transaction.executed_at.year)

    option_tax_summary.revenue += tax_calculation.revenue
    option_tax_summary.cost += tax_calculation.cost
    option_tax_summary.profit_or_loss += tax_calculation.profit_or_loss
    option_tax_summary.tax += tax_calculation.tax
    option_tax_summary.save()

    tax_calculation.tax_summary = option_tax_summary
    tax_calculation.save()
