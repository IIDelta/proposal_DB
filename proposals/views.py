from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Proposal, SOW, Questionnaire, StandardizedQuestionnaire
from django.db.models import Count
from .forms import ProposalForm, SOWForm, QuestionnaireForm, StandardizedQuestionnaireForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


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
    
class StandardizedQuestionnaireListView(ListView):
    model = StandardizedQuestionnaire
    template_name = 'proposals/questionnaires/standardized_questionnaire_list.html'
    context_object_name = 'standardized_names'
    paginate_by = 25

    def get_queryset(self):
        # Annotate with the count of questionnaire quotes using each name
        return StandardizedQuestionnaire.objects.annotate(
            quotes_count=Count('quotes') # 'quotes' is the related_name from Questionnaire.name ForeignKey
        ).order_by('name')


class StandardizedQuestionnaireCreateView(SuccessMessageMixin, CreateView):
    model = StandardizedQuestionnaire
    form_class = StandardizedQuestionnaireForm
    template_name = 'proposals/questionnaires/standardized_questionnaire_form.html'
    success_url = reverse_lazy('standardized_questionnaire_list')
    success_message = "Standardized questionnaire name '%(name)s' was created successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Add New Standardized Questionnaire Name"
        return context


class StandardizedQuestionnaireUpdateView(SuccessMessageMixin, UpdateView):
    model = StandardizedQuestionnaire
    form_class = StandardizedQuestionnaireForm
    template_name = 'proposals/questionnaires/standardized_questionnaire_form.html'
    success_url = reverse_lazy('standardized_questionnaire_list')
    success_message = "Standardized questionnaire name '%(name)s' was updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f"Edit: {self.object.name}"
        return context


class StandardizedQuestionnaireDeleteView(DeleteView):
    model = StandardizedQuestionnaire
    template_name = 'proposals/questionnaires/standardized_questionnaire_confirm_delete.html'
    success_url = reverse_lazy('standardized_questionnaire_list')
    context_object_name = 'standardized_name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the name is in use
        context['is_in_use'] = self.object.quotes.exists() # 'quotes' is related_name
        return context

    def form_valid(self, form):
        # on_delete=models.PROTECT will raise ProtectedError if deletion is not allowed.
        # Django's DeleteView handles this by default and will show an error if PROTECT is violated.
        try:
            # Store name for success message before object is deleted
            name = self.object.name
            response = super().form_valid(form)
            messages.success(self.request, f"Standardized questionnaire name '{name}' deleted successfully.")
            return response
        except models.ProtectedError as e:
            messages.error(self.request, 
                           f"Cannot delete '{self.object.name}' because it is in use by one or more questionnaire quotes. "
                           "Please update or remove those quotes first.")
            return redirect(self.success_url) # Or redirect to the object's detail/edit page


@require_POST # Keep this to ensure the view only accepts POST requests
def ajax_create_standardized_name(request):
    # REMOVED: The check for request.user.is_authenticated
    # if not request.user.is_authenticated: 
    #     return JsonResponse({'success': False, 'error': 'Authentication required.'}, status=403)
        
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        abbreviation = data.get('abbreviation', '').strip()

        if not name:
            return JsonResponse({'success': False, 'error': 'Name cannot be empty.'}, status=400)

        # Use get_or_create to handle cases where the name might have just been added
        # by another concurrent request or if it already exists with a different case.
        # For a unique, case-insensitive check before creation:
        existing_obj = StandardizedQuestionnaire.objects.filter(name__iexact=name).first()
        if existing_obj:
            # Name already exists (case-insensitive)
            return JsonResponse({
                'success': True, 
                'id': existing_obj.id, 
                'name': existing_obj.name,
                'message': 'Name already exists, selected existing.'
            })
        
        new_std_name = StandardizedQuestionnaire.objects.create(
            name=name,
            abbreviation=abbreviation or None 
        )
        return JsonResponse({'success': True, 'id': new_std_name.id, 'name': new_std_name.name})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        # It's good practice to log the actual error `e` on the server for debugging
        # import logging
        # logging.error(f"Error in ajax_create_standardized_name: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred on the server.'}, status=500)
