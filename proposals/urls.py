# proposals/urls.py
from django.urls import path
from .views import (
    SOWListView, SOWDetailView, SOWCreateView, SOWUpdateView, SOWDeleteView,
    ProposalCreateView, ProposalDeleteView
)

urlpatterns = [
    # SOW routes
    path('', SOWListView.as_view(), name='sow_list'),
    path('sow/<int:pk>/', SOWDetailView.as_view(), name='sow_detail'),
    path('sow/create/', SOWCreateView.as_view(), name='sow_create'),
    path('sow/<int:pk>/update/', SOWUpdateView.as_view(), name='sow_update'),
    path('sow/<int:pk>/delete/', SOWDeleteView.as_view(), name='sow_delete'),

    # Proposal routes
    path('proposal/create/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposal/<int:pk>/delete/', ProposalDeleteView.as_view(), name='proposal_delete'),
]
