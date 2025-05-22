# proposals/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class SharedProposalData(models.Model):

    SERVICE_LEVEL_CHOICES = [
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    ]

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
    rfp = models.BooleanField(
        default=False, help_text="Check if this SOW is an RFP")

    # Preparation Checklist Fields
    proposed_service_level = models.CharField(
        max_length=10,
        choices=SERVICE_LEVEL_CHOICES,
        null=True,  # Allow it to be empty initially
        blank=True,  # Allow it to be empty in forms/admin
        default=None  # Or set a default like 'Bronze' if desired
    )
    budget_lower_limit = models.IntegerField(null=True, blank=True)
    budget_upper_limit = models.IntegerField(null=True, blank=True)
    proposal_due_date = models.DateField(null=True, blank=True)
    primary_objective = models.TextField(blank=True)
    vendors_identified = models.JSONField(null=True, blank=True)
    sample_size = models.IntegerField(null=True, blank=True)
    sample_size_justification = models.TextField(blank=True)
    recruitment_duration_value = models.IntegerField(null=True, blank=True)
    recruitment_duration_unit = models.CharField(max_length=20, default='days')

    class Meta:
        abstract = True  # Make this model abstract


class Proposal(SharedProposalData):
    # Enforce format: exactly 4 digits,
    # a hyphen, 1-4 letters, a hyphen, 'P', and exactly 2 digits.
    proposal_id_validator = RegexValidator(
        regex=r'^[0-9]{2}-[a-zA-Z]+-P[0-9]{2}$',
        message=(
            "Proposal ID must be in the format"
            " 'YY-test-PNN' (e.g., 25-test-P01)"
        )
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


class SOW(SharedProposalData):
    # Validator to ensure that the sow_id
    # ends with "-S" followed by two digits.
    sow_id_validator = RegexValidator(
        regex=r'^.*-S\d{2}$',
        message=(
            "SOW ID must end with '-S' "
            "followed by exactly two digits (e.g., -S01)."
        )
    )

    proposal = models.ForeignKey(
        'Proposal', on_delete=models.CASCADE, related_name='sows')
    sow_id = models.CharField(
        max_length=60, unique=True, validators=[sow_id_validator])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Ensure that the sow_id starts
        with the associated proposal's proposal_id.
        """
        if self.proposal and not self.sow_id.startswith(
                self.proposal.proposal_id
                ):
            raise ValidationError(
                f"SOW ID must start with the Proposal ID ("
                f"{self.proposal.proposal_id}"
                ")."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforce validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sow_id


class StandardizedQuestionnaire(models.Model):
    name = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="The official/full name of the questionnaire, e.g., 'Profile of Mood States (POMS)'"
    )
    abbreviation = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Common abbreviation, e.g., 'POMS'"
    )
    # Add any other fields you want for a standardized name, like a description
    # description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Questionnaire(models.Model):
    FORMAT_CHOICES = [
        ('Paper', 'Paper'),
        ('Electronic', 'Electronic'),
    ]

    name = models.ForeignKey(
        StandardizedQuestionnaire, 
        on_delete=models.PROTECT, # Good choice to prevent deletion if in use
        related_name='quotes',
        help_text="Select the standardized questionnaire name."
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price quoted for questionnaire licensing (CAD)")
    date_quoted = models.DateField()
    participants = models.IntegerField(help_text="Number of participants the quote is for")
    administrations_per_participant = models.IntegerField(help_text="Number of questionnaire administrations per participant")
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, help_text="Format of the questionnaire")
    proposal = models.ForeignKey(
        'Proposal', # Assuming Proposal is in the same models.py or correctly imported
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questionnaires',
        help_text="Proposal ID this quote was for (optional)"
    )
    comments = models.TextField(blank=True, null=True, help_text="Any additional comments or notes for this questionnaire quote.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        standardized_name_display = self.name.name if self.name else 'N/A'
        proposal_id_display = self.proposal.proposal_id if self.proposal else 'N/A'
        return f"{standardized_name_display} - Quote for {proposal_id_display}"

    class Meta:
        ordering = ['-date_quoted', 'name__name']
