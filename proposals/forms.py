from django import forms
from .models import Proposal, SOW, SharedProposalData, Questionnaire


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


class QuestionnaireForm(forms.ModelForm):
    date_quoted = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=True
    )
    
    proposal = forms.ModelChoiceField(
        queryset=Proposal.objects.all(),
        to_field_name="proposal_id",
        required=False, # Make it optional as per model
        label="Proposal (Optional)",
        help_text="Select the proposal this quote is for. Type to search by Proposal ID.",
        widget=forms.Select(attrs={'class': 'form-control select2-dropdown'}) # Using a generic class, you might need to initialize select2 JS
    )

    class Meta:
        model = Questionnaire
        fields = [
            'name',
            'price',
            'date_quoted',
            'participants',
            'administrations_per_participant',
            'format',
            'proposal',
            'comments'  # <-- ADDED 'comments'
        ]
        labels = {
            'price': 'Price (CAD)',
            'administrations_per_participant': 'Administrations per Participant',
            'name': 'Questionnaire Name',
            'comments': 'Comments / Notes', # <-- Optional: Custom label

        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., GSRS, POMS'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'participants': forms.NumberInput(attrs={'placeholder': 'e.g., 100'}),
            'administrations_per_participant': forms.NumberInput(attrs={'placeholder': 'e.g., 1'}),
            'format': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter any relevant comments here...'}), # <-- Optional: Use Textarea widget
        }
        help_texts = {
            'proposal': 'Leave blank if this is a general quote not tied to a specific proposal.'
        }

    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        # Make proposal field not required by default if it's optional in model
        if self.fields['proposal'].required:
             self.fields['proposal'].required = False # Double ensure it's not required if blank=True, null=True