# Generated by Django 5.0.1 on 2024-03-25 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_currencyratefile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currencyratefile',
            options={'verbose_name': 'Currency rate file 💵', 'verbose_name_plural': 'Currency rate files 💵'},
        ),
        migrations.AlterModelOptions(
            name='reportfile',
            options={'verbose_name': 'Report file 📊', 'verbose_name_plural': 'Report files 📊'},
        ),
    ]