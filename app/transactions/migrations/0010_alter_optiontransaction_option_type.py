# Generated by Django 5.0.1 on 2024-04-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_optiontransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optiontransaction',
            name='option_type',
            field=models.CharField(blank=True, choices=[('CALL', 'CALL'), ('PUT', 'PUT')], max_length=4),
        ),
    ]
