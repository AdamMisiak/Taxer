from tax_summaries.models import AsssetTaxSummary
from tax_calculations.models import AssetTaxCalculation

def _get_asset_tax_summary(tax_year: int) -> AsssetTaxSummary:
    asset_tax_summary, _ = AsssetTaxSummary.objects.get_or_create(
        year=tax_year,
        defaults={'revenue': 0, 'cost': 0, "profit_or_loss": 0, 'tax': 0}
    )
    return asset_tax_summary


def assign_asset_tax_summary(tax_calculation: AssetTaxCalculation):
    asset_tax_summary = _get_asset_tax_summary(tax_calculation.closing_transaction.executed_at.year)

    asset_tax_summary.revenue += tax_calculation.revenue
    asset_tax_summary.cost += tax_calculation.cost
    asset_tax_summary.profit_or_loss += tax_calculation.profit_or_loss
    asset_tax_summary.tax += tax_calculation.tax
    asset_tax_summary.save()

    tax_calculation.tax_summary = asset_tax_summary
    tax_calculation.save()
