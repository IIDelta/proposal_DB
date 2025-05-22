from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Proposal, SOW, Questionnaire
from .forms import ProposalForm, SOWForm, QuestionnaireForm


# Combined listing view: lists proposals and their associated SOWs.
class SOWListView(ListView):
    model = Proposal
    template_name = 'proposals/sow_list.html'
    context_object_name = 'proposals'
    queryset = Proposal.objects.all().prefetch_related('sows')

    def get_queryset(self):
        queryset = Proposal.objects.all().prefetch_related('sows')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(proposal_id__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide all proposal IDs for the autocomplete datalist.
        context['all_proposals'] = Proposal.objects.values_list('proposal_id', flat=True)
        return context


# Proposal CRUD Views
class ProposalCreateView(CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "Proposal created successfully.")
        return super().form_valid(form)


class ProposalUpdateView(UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "Proposal updated successfully.")
        return super().form_valid(form)


class ProposalDeleteView(DeleteView):
    model = Proposal
    template_name = 'proposals/proposal_confirm_delete.html'
    success_url = reverse_lazy('proposal_sow_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Proposal deleted successfully.")
        return super().delete(request, *args, **kwargs)


# SOW CRUD Views
class SOWDetailView(DetailView):
    model = SOW
    template_name = 'proposals/sow_detail.html'
    context_object_name = 'sow'


class SOWCreateView(CreateView):
    model = SOW
    form_class = SOWForm
    template_name = 'proposals/sow_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_proposals'] = Proposal.objects.all()
        return context


class SOWUpdateView(UpdateView):
    model = SOW
    form_class = SOWForm
    template_name = 'proposals/sow_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "SOW updated successfully.")
        return super().form_valid(form)


class SOWDeleteView(DeleteView):
    model = SOW
    template_name = 'proposals/sow_confirm_delete.html'
    success_url = reverse_lazy('proposal_sow_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "SOW deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ProposalDetailView(DetailView):
    model = Proposal
    template_name = 'proposals/proposal_detail.html'
    context_object_name = 'proposal'  # Use 'proposal' in the template context


# Questionnaire CRUD Views
class QuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'proposals/questionnaires/questionnaire_list.html'
    context_object_name = 'questionnaires'
    paginate_by = 20 # Optional

    def get_queryset(self):
        # Order by date_quoted descending, then by name ascending
        return Questionnaire.objects.select_related('proposal').all().order_by('-date_quoted', 'name')


class QuestionnaireDetailView(DetailView):
    model = Questionnaire
    template_name = 'proposals/questionnaires/questionnaire_detail.html'
    context_object_name = 'questionnaire'


class QuestionnaireCreateView(CreateView):
    model = Questionnaire
    form_class = QuestionnaireForm
    template_name = 'proposals/questionnaires/questionnaire_form.html'
    success_url = reverse_lazy('questionnaire_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add New Questionnaire Quote"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Questionnaire quote created successfully.")
        return super().form_valid(form)


class QuestionnaireUpdateView(UpdateView):
    model = Questionnaire
    form_class = QuestionnaireForm
    template_name = 'proposals/questionnaires/questionnaire_form.html'
    success_url = reverse_lazy('questionnaire_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Edit Quote: {self.object.name}"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Questionnaire quote updated successfully.")
        return super().form_valid(form)


class QuestionnaireDeleteView(DeleteView):
    model = Questionnaire
    template_name = 'proposals/questionnaires/questionnaire_confirm_delete.html'
    success_url = reverse_lazy('questionnaire_list')
    context_object_name = 'questionnaire'

    def form_valid(self, form): # Use form_valid for success message consistency with DeleteView
        messages.success(self.request, f"Questionnaire quote '{self.object.name}' deleted successfully.")
        return super().form_valid(form)