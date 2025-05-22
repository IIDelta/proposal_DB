from django import forms
from .models import Proposal, SOW, SharedProposalData, Questionnaire, StandardizedQuestionnaire


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
    # This is the dropdown for existing standardized names
    name = forms.ModelChoiceField(
        queryset=StandardizedQuestionnaire.objects.all(),
        required=False,  # Will be made effectively required by clean() if new_name not provided
        widget=forms.Select(attrs={'class': 'form-control select2-dropdown'}),
        label="Standardized Questionnaire Name"
    )
    # New field to add a new standardized name
    new_standardized_name = forms.CharField(
        required=False,
        label="Add new questionnaire name (if required)",
        help_text="If the questionnaire name is not in the list above, type its full official name here. An abbreviation can be added via the admin panel later.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Profile of Mood States (POMS)'})
    )
    # New field for the abbreviation if adding a new standardized name
    new_standardized_abbreviation = forms.CharField(
        required=False,
        label="Abbreviation for new name (optional)",
        help_text="Enter a common abbreviation if adding a new questionnaire name.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., POMS'})
    )

    date_quoted = forms.DateField(
        widget=CustomDateInput(),
        input_formats=['%Y-%m-%d'],
        required=True
    )
    proposal = forms.ModelChoiceField(
        queryset=Proposal.objects.all(),
        to_field_name="proposal_id",
        required=False, 
        label="Proposal (Optional)",
        help_text="Select the proposal this quote is for. Type to search by Proposal ID.",
        widget=forms.Select(attrs={'class': 'form-control select2-dropdown'})
    )

    class Meta:
        model = Questionnaire
        fields = [
            'name', # This is the ForeignKey, will be populated by dropdown or new_standardized_name
            # new_standardized_name and new_standardized_abbreviation are not model fields, handled in clean()
            'price',
            'date_quoted',
            'participants',
            'administrations_per_participant',
            'format',
            'proposal',
            'comments'
        ]
        # Labels for model fields can be defined here if not already on the model or if you want to override
        labels = {
            'price': 'Price (CAD)',
            'administrations_per_participant': 'Administrations per Participant',
            'comments': 'Comments / Notes',
        }
        widgets = {
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'participants': forms.NumberInput(attrs={'placeholder': 'e.g., 100'}),
            'administrations_per_participant': forms.NumberInput(attrs={'placeholder': 'e.g., 1'}),
            'format': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter any relevant comments here...'}),
        }
        help_texts = {
            'proposal': 'Leave blank if this is a general quote not tied to a specific proposal.'
        }

    # To ensure new fields are ordered nicely with crispy-forms, you might need a Layout helper
    # Or adjust their order in the `fields` list declaration above if not using Meta.fields
    # For now, let's explicitly order them if needed by overriding the field order attribute
    # (This is more for manual rendering or basic crispy rendering; Layout is better for complex crispy ordering)

    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        # Define field order if not using a crispy_forms.helper.Layout
        # The order is name (dropdown), new_standardized_name, new_standardized_abbreviation, then the rest
        field_order = [
            'name', 'new_standardized_name', 'new_standardized_abbreviation', 
            'price', 'date_quoted', 'participants', 'administrations_per_participant', 
            'format', 'proposal', 'comments'
        ]
        # self.fields = {f: self.fields[f] for f in field_order if f in self.fields} # This reorders
        # A simpler way for crispy is often to use a Layout helper. For now, let's assume crispy handles it or you'll adjust the template.
        
        if 'proposal' in self.fields and self.fields['proposal'].required:
             self.fields['proposal'].required = False
        
        # For crispy forms, it's better to add non-model fields explicitly to the layout helper if you need precise control.
        # Otherwise, crispy should pick them up if they are declared on the form class.

    def clean(self):
        cleaned_data = super().clean()
        name_dropdown = cleaned_data.get('name')
        new_name_text = cleaned_data.get('new_standardized_name')
        new_abbreviation_text = cleaned_data.get('new_standardized_abbreviation')

        if new_name_text:
            # User is trying to add a new standardized name
            if name_dropdown:
                # User selected from dropdown AND typed a new name - this is ambiguous
                self.add_error('new_standardized_name', 
                               "Please either select an existing name from the dropdown or enter a new name, but not both.")
                self.add_error('name',
                               "Please either select an existing name from the dropdown or enter a new name, but not both.")
            else:
                # Create or get the StandardizedQuestionnaire instance
                standardized_questionnaire, created = StandardizedQuestionnaire.objects.get_or_create(
                    name=new_name_text,
                    defaults={'abbreviation': new_abbreviation_text or None} # Use abbreviation if provided
                )
                if not created and new_abbreviation_text and standardized_questionnaire.abbreviation != new_abbreviation_text:
                    # Name exists, but user might be trying to set/change abbreviation via this form.
                    # Decide on behavior: update abbreviation, ignore, or error.
                    # For simplicity, let's assume if the name exists, we use it as-is.
                    # Abbreviation management can be done via admin for existing names.
                    pass 
                cleaned_data['name'] = standardized_questionnaire # Set the FK field to this instance
        elif not name_dropdown:
            # No new name typed, and no existing name selected from dropdown
            self.add_error('name', "This field is required. Please select a questionnaire name or add a new one below.")
        
        return cleaned_data


# New Form for StandardizedQuestionnaire
class StandardizedQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = StandardizedQuestionnaire
        fields = ['name', 'abbreviation'] # Add any other fields like 'description' if you added them to the model
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full official name, e.g., Profile of Mood States (POMS)'}),
            'abbreviation': forms.TextInput(attrs={'placeholder': 'Common abbreviation, e.g., POMS'}),
            # 'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Standardized Full Name',
            'abbreviation': 'Abbreviation (Optional)',
        }
        help_texts = {
            'name': 'This name will be used in dropdowns. Ensure it is accurate and unique.',
        }