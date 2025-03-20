from django import forms
from .models import Proposal, SOW


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['proposal_id']  # Only the ID for creation/deletion


class CustomDateInput(forms.DateInput):
    format = '%Y.%m.%d'
    input_type = 'text'


RECRUITMENT_UNIT_CHOICES = [
    ('weeks', 'Weeks'),
    ('months', 'Months'),
]


class SOWForm(forms.ModelForm):
    date_questionnaire_issued = forms.DateField(
        widget=CustomDateInput(attrs={'placeholder': 'YYYY.MM.DD'}),
        input_formats=['%Y.%m.%d'],
        required=False
    )
    study_design_approval_date = forms.DateField(
        widget=CustomDateInput(attrs={'placeholder': 'YYYY.MM.DD'}),
        input_formats=['%Y.%m.%d'],
        required=False
    )
    pricing_approval_date = forms.DateField(
        widget=CustomDateInput(attrs={'placeholder': 'YYYY.MM.DD'}),
        input_formats=['%Y.%m.%d'],
        required=False
    )
    final_proposal_approval_date = forms.DateField(
        widget=CustomDateInput(attrs={'placeholder': 'YYYY.MM.DD'}),
        input_formats=['%Y.%m.%d'],
        required=False
    )
    proposal_due_date = forms.DateField(
        widget=CustomDateInput(attrs={'placeholder': 'YYYY.MM.DD'}),
        input_formats=['%Y.%m.%d'],
        required=False
    )
    recruitment_duration_unit = forms.ChoiceField(
        choices=RECRUITMENT_UNIT_CHOICES,
        required=False
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
        help_text="Enter vendors as a comma separated list, e.g., Vendor1, Vendor2, Vendor3."
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
        # Override the initial value for the proposal field using self.initial
        if self.instance and self.instance.pk and self.instance.proposal:
            self.initial['proposal'] = self.instance.proposal.proposal_id

    def clean_proposal(self):
        proposal_id = self.cleaned_data.get('proposal')
        try:
            proposal_instance = Proposal.objects.get(proposal_id=proposal_id)
        except Proposal.DoesNotExist:
            raise forms.ValidationError("Proposal with this ID does not exist.")
        return proposal_instance

    def clean_vendors_identified(self):
        data = self.cleaned_data.get('vendors_identified', '')
        if data:
            vendor_list = [v.strip() for v in data.split(',') if v.strip()]
            return vendor_list
        return []
