
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv

from transactions.models import ImportFile

@receiver(post_save, sender=ImportFile)
def save_transactions_from_the_file(sender, instance, *args, **kwargs):
    print(instance)
    print(instance.file)
    # import_file_object = ImportFile.objects.get(id=1)
    # print(import_file_object)
    print('post save callback I AM HERE')
    with instance.file.open('r') as file:
        # lines = f.readlines()
        # print(lines)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
            print(row)

