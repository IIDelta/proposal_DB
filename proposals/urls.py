from django.urls import path
from .views import (
    SOWListView,
    ProposalCreateView, 
    ProposalUpdateView, 
    ProposalDeleteView,
    SOWDetailView, 
    SOWCreateView, 
    SOWUpdateView, 
    SOWDeleteView
)

urlpatterns = [
    # Combined view: proposals and their SOWs
    path('proposals/', SOWListView.as_view(), name='proposal_sow_list'),
    
    # Proposal CRUD URLs
    path('proposal/create/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposal/<int:pk>/update/', ProposalUpdateView.as_view(), name='proposal_update'),
    path('proposal/<int:pk>/delete/', ProposalDeleteView.as_view(), name='proposal_delete'),
    
    # SOW URLs
    path('', SOWListView.as_view(), name='sow_list'),
    path('sow/<int:pk>/', SOWDetailView.as_view(), name='sow_detail'),
    path('sow/create/', SOWCreateView.as_view(), name='sow_create'),
    path('sow/<int:pk>/update/', SOWUpdateView.as_view(), name='sow_update'),
    path('sow/<int:pk>/delete/', SOWDeleteView.as_view(), name='sow_delete'),
]
