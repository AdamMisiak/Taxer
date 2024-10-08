# Generated by Django 5.0.1 on 2024-09-29 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax_summaries', '0008_dividendtaxsummary_profit_or_loss'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestRateTaxSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('cost', models.FloatField(blank=True, null=True)),
                ('profit_or_loss', models.FloatField(blank=True, null=True)),
                ('tax', models.FloatField(blank=True, null=True)),
                ('general_tax_summary', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interest_rate_tax_summaries', to='tax_summaries.generaltaxsummary')),
            ],
            options={
                'verbose_name': 'Interest rate tax summary ➕',
                'verbose_name_plural': 'Interest rate tax summaries ➕',
            },
        ),
    ]
