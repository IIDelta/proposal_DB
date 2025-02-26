from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Proposal, SOW
from .forms import ProposalForm, SOWForm

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
class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "Proposal created successfully.")
        return super().form_valid(form)

class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "Proposal updated successfully.")
        return super().form_valid(form)

class ProposalDeleteView(LoginRequiredMixin, DeleteView):
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

class SOWCreateView(LoginRequiredMixin, CreateView):
    model = SOW
    form_class = SOWForm
    template_name = 'proposals/sow_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_proposals'] = Proposal.objects.all()
        return context


class SOWUpdateView(LoginRequiredMixin, UpdateView):
    model = SOW
    form_class = SOWForm
    template_name = 'proposals/sow_form.html'
    success_url = reverse_lazy('proposal_sow_list')

    def form_valid(self, form):
        messages.success(self.request, "SOW updated successfully.")
        return super().form_valid(form)

class SOWDeleteView(LoginRequiredMixin, DeleteView):
    model = SOW
    template_name = 'proposals/sow_confirm_delete.html'
    success_url = reverse_lazy('proposal_sow_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "SOW deleted successfully.")
        return super().delete(request, *args, **kwargs)
