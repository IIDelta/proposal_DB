# proposals/models.py
from django.db import models
from django.core.exceptions import ValidationError

class Proposal(models.Model):
    proposal_id = models.CharField(max_length=50, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.proposal_id

class SOW(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='sows')
    sow_id = models.CharField(max_length=60, unique=True)
    
    # BD Data Fields
    date_questionnaire_issued = models.DateField(null=True, blank=True)
    bid_defense_required = models.BooleanField(default=False)
    bid_defense_results = models.CharField(max_length=255, blank=True)
    mw_assigned_to_synopsis = models.CharField(max_length=255, blank=True)
    study_design_version = models.CharField(max_length=20, blank=True)
    study_design_approval_date = models.DateField(null=True, blank=True)
    pricing_version = models.CharField(max_length=20, blank=True)
    pricing_approval_date = models.DateField(null=True, blank=True)
    final_proposal_version = models.CharField(max_length=20, blank=True)
    final_proposal_approval_date = models.DateField(null=True, blank=True)
    
    # Preparation Checklist Fields
    budget_lower_limit = models.IntegerField(null=True, blank=True)
    budget_upper_limit = models.IntegerField(null=True, blank=True)
    proposal_due_date = models.DateField(null=True, blank=True)
    primary_objective = models.TextField(blank=True)
    vendors_identified = models.JSONField(null=True, blank=True)
    sample_size = models.IntegerField(null=True, blank=True)
    sample_size_justification = models.TextField(blank=True)
    recruitment_duration_value = models.IntegerField(null=True, blank=True)
    recruitment_duration_unit = models.CharField(max_length=20, default='days')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Custom validation to ensure sow_id starts with the proposal's proposal_id
        if self.proposal and not self.sow_id.startswith(self.proposal.proposal_id):
            raise ValidationError(
                f"SOW ID must start with the Proposal ID ({self.proposal.proposal_id})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforce model validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sow_id
