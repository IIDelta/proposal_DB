from django import forms
from .models import Proposal, SOW, SharedProposalData


class CustomDateInput(forms.DateInput):
    input_type = 'date' # USE HTML5 DATE INPUT


RECRUITMENT_UNIT_CHOICES = [
    ('weeks', 'Weeks'),
    ('months', 'Months'),
]


class ProposalForm(forms.ModelForm):
    date_questionnaire_issued = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    study_design_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    pricing_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    final_proposal_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    proposal_due_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    recruitment_duration_unit = forms.ChoiceField(
        choices=RECRUITMENT_UNIT_CHOICES,
        required=False
    )
    proposed_service_level = forms.ChoiceField(
        choices=[('', '---------')] + SharedProposalData.SERVICE_LEVEL_CHOICES,  # Add an empty choice
        required=False,  # Make it optional if desired
        widget=forms.Select(attrs={'class': 'form-control'})  # Use standard dropdown
    )
    budget_lower_limit = forms.IntegerField(
        required=False,
        label="Budget Lower Limit (CAD)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter lower limit in CAD'})
    )
    budget_upper_limit = forms.IntegerField(
        required=False,
        label="Budget Upper Limit (CAD)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter upper limit in CAD'})
    )
    rfp = forms.BooleanField(
        required=False,
        label="RFP",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check if this SOW is an RFP"
    )
    bid_defense_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    vendors_identified = forms.CharField(
        required=False,
        label="Vendors Identified (comma separated)",
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter vendors, separated by commas',
            'rows': 5
        }),
        help_text="Enter vendors as a comma separated list" \
        ", e.g., Vendor1, Vendor2, Vendor3."
    )

    class Meta:
        model = Proposal
        fields = '__all__' # Include proposal_id and all inherited fields
        # Optional: Copy clean_vendors_identified method 
        # if you want that validation here too

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        # Check if instance exists and has vendors_identified data
        if self.instance and self.instance.pk and isinstance(self.instance.vendors_identified, list):
            # Convert list to comma-separated string for display in the textarea
            self.initial['vendors_identified'] = ', '.join(self.instance.vendors_identified)
        elif self.instance and self.instance.pk and self.instance.vendors_identified is None:
            # Ensure None is treated as an empty string for the form field
            self.initial['vendors_identified'] = ''

    def clean_vendors_identified(self):
        data = self.cleaned_data.get('vendors_identified', '')
        if data and isinstance(data, str):
            vendor_list = [v.strip() for v in data.split(',') if v.strip()]
            return vendor_list
        elif isinstance(data, list):  # Already processed?
            return data
        return []


class SOWForm(forms.ModelForm):
    date_questionnaire_issued = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    study_design_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    pricing_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    final_proposal_approval_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    proposal_due_date = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    recruitment_duration_unit = forms.ChoiceField(
        choices=RECRUITMENT_UNIT_CHOICES,
        required=False
    )
    proposed_service_level = forms.ChoiceField(
        choices=[('', '---------')] + SharedProposalData.SERVICE_LEVEL_CHOICES,  # Add an empty choice
        required=False,  # Make it optional if desired
        widget=forms.Select(attrs={'class': 'form-control'})  # Use standard dropdown
    )
    budget_lower_limit = forms.IntegerField(
        required=False,
        label="Budget Lower Limit (CAD)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter lower limit in CAD'})
    )
    budget_upper_limit = forms.IntegerField(
        required=False,
        label="Budget Upper Limit (CAD)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter upper limit in CAD'})
    )
    rfp = forms.BooleanField(
        required=False,
        label="RFP",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check if this SOW is an RFP"
    )
    bid_defense_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    vendors_identified = forms.CharField(
        required=False,
        label="Vendors Identified (comma separated)",
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter vendors, separated by commas',
            'rows': 5
        }),
        help_text="Enter vendors as a comma separated list," \
        " e.g., Vendor1, Vendor2, Vendor3."
    )
    # Use a text field for proposal selection
    proposal = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Proposal ID',
            'list': 'proposalList'
        }),
    )

    class Meta:
        model = SOW
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SOWForm, self).__init__(*args, **kwargs)
        # Handle proposal field initial value (as before)
        if self.instance and self.instance.pk and self.instance.proposal:
            self.initial['proposal'] = self.instance.proposal.proposal_id

        # Handle vendors_identified display (NEW PART)
        if self.instance and self.instance.pk and isinstance(self.instance.vendors_identified, list):
            # Convert list to comma-separated string for display
            self.initial['vendors_identified'] = ', '.join(self.instance.vendors_identified)
        elif self.instance and self.instance.pk and self.instance.vendors_identified is None:
             # Ensure None is treated as an empty string for the form field
            self.initial['vendors_identified'] = ''

    def clean_proposal(self):
        proposal_id = self.cleaned_data.get('proposal')
        try:
            proposal_instance = Proposal.objects.get(proposal_id=proposal_id)
        except Proposal.DoesNotExist:
            raise forms.ValidationError("Proposal with this ID does not exist.")
        return proposal_instance

    def clean_vendors_identified(self):
        data = self.cleaned_data.get('vendors_identified', '')
        # Check if data is already a list
        if isinstance(data, list):
            return data
        if data and isinstance(data, str):
            # Split the string from the textarea into a list
            vendor_list = [v.strip() for v in data.split(',') if v.strip()]
            return vendor_list
        return [] # Return an empty list if input is empty/whitespace
