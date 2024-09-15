from tax_summaries.models import GeneralTaxSummary, AssetTaxSummary, DividendTaxSummary, OptionTaxSummary
# from tax_calculations.models import BaseTaxCalculation

def _get_general_tax_summary(tax_year: int) -> GeneralTaxSummary:
    general_tax_summary, _ = GeneralTaxSummary.objects.get_or_create(
        year=tax_year,
        defaults={'revenue': 0, 'cost': 0, 'profit_or_loss': 0, 'tax': 0}
    )
    return general_tax_summary


def assign_general_tax_summary(tax_summary: AssetTaxSummary | OptionTaxSummary):
    general_tax_summary = _get_general_tax_summary(tax_summary.year)

    general_tax_summary.revenue += tax_summary.revenue
    general_tax_summary.cost += tax_summary.cost
    general_tax_summary.profit_or_loss += tax_summary.profit_or_loss
    general_tax_summary.tax += tax_summary.tax
    general_tax_summary.save()

    tax_summary.general_tax_summary = general_tax_summary
    tax_summary.save()

def assign_general_tax_summary_to_dividend_tax_summary(tax_summary: DividendTaxSummary):
    general_tax_summary = _get_general_tax_summary(tax_summary.year)

    general_tax_summary.revenue += tax_summary.revenue
    general_tax_summary.cost += tax_summary.tax_paid
    general_tax_summary.profit_or_loss += tax_summary.profit_or_loss
    general_tax_summary.tax += tax_summary.tax
    general_tax_summary.save()

    tax_summary.general_tax_summary = general_tax_summary
    tax_summary.save()