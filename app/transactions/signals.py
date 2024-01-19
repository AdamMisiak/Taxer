from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.logic import calculate_tax_to_pay, save_data_from_file, update_tax_summary_for_year
from transactions.models import ImportFile, TaxCalculation, Transaction


@receiver(post_save, sender=ImportFile)
def save_data_from_file_signal(sender, instance, *args, **kwargs):
    save_data_from_file(instance)


@receiver(post_save, sender=Transaction)
def calculate_tax_to_pay_signal(sender, instance, *args, **kwargs):
    calculate_tax_to_pay(instance)


@receiver(post_save, sender=TaxCalculation)
def update_tax_summary_for_year_signal(sender, instance, *args, **kwargs):
    update_tax_summary_for_year(instance)
