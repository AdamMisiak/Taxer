# def init_tax_summary(tax_year: int):
#     if not TaxSummary.objects.filter(year=tax_year).exists():
#         TaxSummary.objects.create(year=tax_year, revenue_equity=0, revenue_dividend=0, cost_equity=0, tax_paid_dividend=0, tax_equity=0, tax_dividend=0)
