from django.contrib import admin
from .models import Proposal, SOW

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


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(SOW, SOWAdmin)
