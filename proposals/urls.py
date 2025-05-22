from django.urls import path
from .views import (
    SOWListView,
    ProposalCreateView,
    ProposalUpdateView,
    ProposalDeleteView,
    SOWDetailView,
    SOWCreateView,
    SOWUpdateView,
    SOWDeleteView,
    ProposalDetailView,
    QuestionnaireListView, QuestionnaireDetailView, QuestionnaireCreateView,
    QuestionnaireUpdateView, QuestionnaireDeleteView
)

urlpatterns = [
    # Combined view: proposals and their SOWs
    path('', SOWListView.as_view(), name='proposal_sow_list'),

    # Proposal CRUD URLs
    path('proposal/create/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposal/<int:pk>/update/', ProposalUpdateView.as_view(), name='proposal_update'),
    path('proposal/<int:pk>/delete/', ProposalDeleteView.as_view(), name='proposal_delete'),
    path('proposal/<int:pk>/', ProposalDetailView.as_view(), name='proposal_detail'),

    # SOW URLs
    path('proposals/', SOWListView.as_view(), name='sow_list'),
    path('sow/<int:pk>/', SOWDetailView.as_view(), name='sow_detail'),
    path('sow/create/', SOWCreateView.as_view(), name='sow_create'),
    path('sow/<int:pk>/update/', SOWUpdateView.as_view(), name='sow_update'),
    path('sow/<int:pk>/delete/', SOWDeleteView.as_view(), name='sow_delete'),

    # Questionnaire URLs - these will be prefixed by how 'proposals.urls' is included in your project's main urls.py
    # To achieve proposals.local/questionnaires/, this file should be included at the root or with a prefix
    # that allows this structure.
    path('questionnaires/', QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('questionnaires/create/', QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('questionnaires/<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('questionnaires/<int:pk>/update/', QuestionnaireUpdateView.as_view(), name='questionnaire_update'),
    path('questionnaires/<int:pk>/delete/', QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
]
