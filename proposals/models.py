# proposals/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Proposal(models.Model):
    # Enforce format: exactly 4 digits, a hyphen, 1-4 letters, a hyphen, 'P', and exactly 2 digits.
    proposal_id_validator = RegexValidator(
        regex=r'^\d{4}-[A-Za-z]{1,4}-P\d{2}$',
        message="Proposal ID must be in the format 'XXXX-text-PXX', where X are digits and 'text' is 1 to 4 letters."
    )
    proposal_id = models.CharField(
        max_length=50,
        unique=True,
        validators=[proposal_id_validator]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.proposal_id

class SOW(models.Model):
    # Validator to ensure that the sow_id ends with "-S" followed by two digits.
    sow_id_validator = RegexValidator(
        regex=r'^.*-S\d{2}$',
        message="SOW ID must end with '-S' followed by exactly two digits (e.g., -S01)."
    )
    
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, related_name='sows')
    sow_id = models.CharField(max_length=60, unique=True, validators=[sow_id_validator])
    
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
        """
        Ensure that the sow_id starts with the associated proposal's proposal_id.
        """
        if self.proposal and not self.sow_id.startswith(self.proposal.proposal_id):
            raise ValidationError(
                f"SOW ID must start with the Proposal ID ({self.proposal.proposal_id})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforce validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sow_id