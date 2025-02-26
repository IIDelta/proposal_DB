# proposals/forms.py
from django import forms
from .models import Proposal, SOW

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['proposal_id']  # Only the ID for creation/deletion

class CustomDateInput(forms.DateInput):
    # Force the widget to use our custom format and render as a text input
    format = '%Y.%m.%d'
    input_type = 'text'  # Prevents browsers from overriding with an HTML5 datepicker


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
         widget=forms.NumberInput(attrs={'placeholder': 'Enter lower limit in CAD'})
    )
    budget_upper_limit = forms.IntegerField(
         required=False,
         label="Budget Upper Limit (CAD)",
         widget=forms.NumberInput(attrs={'placeholder': 'Enter upper limit in CAD'})
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

    class Meta:
        model = SOW
        fields = '__all__'

    def clean_vendors_identified(self):
        """
        Convert a comma-separated string of vendors into a Python list.
        This ensures that the data stored in the JSONField is valid.
        """
        data = self.cleaned_data.get('vendors_identified', '')
        if data:
            vendor_list = [v.strip() for v in data.split(',') if v.strip()]
            return vendor_list
        return []
