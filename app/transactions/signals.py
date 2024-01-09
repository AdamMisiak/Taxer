from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.logic import calculate_tax_to_pay, save_data_from_file
from transactions.models import  ImportFile, Transaction


@receiver(post_save, sender=ImportFile)
def save_data_from_file_signal(sender, instance, *args, **kwargs):
    save_data_from_file(instance)


@receiver(post_save, sender=Transaction)
def calculate_tax_to_pay_signal(sender, instance, *args, **kwargs):
    calculate_tax_to_pay(instance)
