# Generated by Django 5.0.1 on 2024-07-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0021_optiontransaction_closing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optiontransaction',
            name='closing',
        ),
        migrations.AddField(
            model_name='assettransaction',
            name='type',
            field=models.CharField(blank=True, choices=[('Opening', 'Opening'), ('Closing', 'Closing')], max_length=16),
        ),
        migrations.AddField(
            model_name='optiontransaction',
            name='type',
            field=models.CharField(blank=True, choices=[('Opening', 'Opening'), ('Closing', 'Closing')], max_length=16),
        ),
    ]
