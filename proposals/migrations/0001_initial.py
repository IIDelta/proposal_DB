# Generated by Django 5.0.12 on 2025-02-26 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal_id', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SOW',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sow_id', models.CharField(max_length=60, unique=True)),
                ('date_questionnaire_issued', models.DateField(blank=True, null=True)),
                ('bid_defense_required', models.BooleanField(default=False)),
                ('bid_defense_results', models.CharField(blank=True, max_length=255)),
                ('mw_assigned_to_synopsis', models.CharField(blank=True, max_length=255)),
                ('study_design_version', models.CharField(blank=True, max_length=20)),
                ('study_design_approval_date', models.DateField(blank=True, null=True)),
                ('pricing_version', models.CharField(blank=True, max_length=20)),
                ('pricing_approval_date', models.DateField(blank=True, null=True)),
                ('final_proposal_version', models.CharField(blank=True, max_length=20)),
                ('final_proposal_approval_date', models.DateField(blank=True, null=True)),
                ('budget_lower_limit', models.IntegerField(blank=True, null=True)),
                ('budget_upper_limit', models.IntegerField(blank=True, null=True)),
                ('proposal_due_date', models.DateField(blank=True, null=True)),
                ('primary_objective', models.TextField(blank=True)),
                ('vendors_identified', models.JSONField(blank=True, null=True)),
                ('sample_size', models.IntegerField(blank=True, null=True)),
                ('sample_size_justification', models.TextField(blank=True)),
                ('recruitment_duration_value', models.IntegerField(blank=True, null=True)),
                ('recruitment_duration_unit', models.CharField(default='days', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sows', to='proposals.proposal')),
            ],
        ),
    ]
