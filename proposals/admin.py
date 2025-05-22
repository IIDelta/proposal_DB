from django.contrib import admin
from .models import Proposal, SOW, Questionnaire

# Inline admin for SOW – allows editing SOW records on a Proposal’s admin page.


class SOWInline(admin.TabularInline):
    model = SOW
    extra = 0  # Change if you want extra empty forms for new SOWs

# Custom admin for Proposal


class ProposalAdmin(admin.ModelAdmin):
    list_display = ('proposal_id', 'created_at', 'updated_at')
    search_fields = ('proposal_id',)
    inlines = [SOWInline]

# Custom admin for SOW


class SOWAdmin(admin.ModelAdmin):
    list_display = ('sow_id', 'proposal', 'created_at')
    search_fields = ('sow_id',)
    list_filter = ('proposal',)


class QuestionnaireInline(admin.TabularInline):
    model = Questionnaire
    extra = 0
    fields = ('name', 'price', 'date_quoted', 'participants', 'administrations_per_participant', 'format', 'comments', 'updated_at') # Add 'comments'
    readonly_fields = ('updated_at',)
    show_change_link = True


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('name', 'proposal_link', 'price', 'date_quoted', 'participants', 'format', 'comments', 'updated_at') # Add 'comments'
    search_fields = ('name', 'proposal__proposal_id', 'comments') # Add 'comments'
    list_filter = ('format', 'date_quoted', 'proposal')
    ordering = ('-date_quoted', 'name')
    autocomplete_fields = ['proposal']
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'proposal', 'price', 'date_quoted', 'comments') # Add 'comments'
        }),
        ('Details', {
            'fields': ('participants', 'administrations_per_participant', 'format')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    # ... (proposal_link method) ...
    def proposal_link(self, obj): # Keep this method if you have it
        if obj.proposal:
            from django.urls import reverse
            from django.utils.html import format_html
            link = reverse("admin:proposals_proposal_change", args=[obj.proposal.id])
            return format_html('<a href="{}">{}</a>', link, obj.proposal.proposal_id)
        return "-"
    proposal_link.short_description = 'Proposal'


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(SOW, SOWAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin) # Register Questionnaire
