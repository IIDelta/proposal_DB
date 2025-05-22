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
    QuestionnaireUpdateView, QuestionnaireDeleteView,
    StandardizedQuestionnaireListView, StandardizedQuestionnaireCreateView,
    StandardizedQuestionnaireUpdateView, StandardizedQuestionnaireDeleteView,
    ajax_create_standardized_name
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

    # URLs for StandardizedQuestionnaire Management
    path('questionnaires/manage-names/',
         StandardizedQuestionnaireListView.as_view(),
         name='standardized_questionnaire_list'),
    path('questionnaires/manage-names/add/',
         StandardizedQuestionnaireCreateView.as_view(),
         name='standardized_questionnaire_create'),
    path('questionnaires/manage-names/<int:pk>/edit/',
         StandardizedQuestionnaireUpdateView.as_view(),
         name='standardized_questionnaire_update'),
    path('questionnaires/manage-names/<int:pk>/delete/',
         StandardizedQuestionnaireDeleteView.as_view(),
         name='standardized_questionnaire_delete'),
    path('ajax/create-standardized-name/',
         ajax_create_standardized_name,
         name='ajax_create_standardized_name'),
]
