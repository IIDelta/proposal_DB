# proposals/forms.py
from django import forms
from .models import Proposal, SOW

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['proposal_id']  # Only the ID for creation/deletion

class SOWForm(forms.ModelForm):
    """
    This form includes a ModelChoiceField for 'proposal' that displays the actual
    proposal_id in the dropdown instead of the default (which is also proposal_id
    since __str__ returns proposal_id, but let's be explicit).
    """
    proposal = forms.ModelChoiceField(
        queryset=Proposal.objects.all(),
        label='Proposal'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure the dropdown label is the actual proposal_id
        self.fields['proposal'].label_from_instance = lambda obj: obj.proposal_id

    class Meta:
        model = SOW
        fields = '__all__'