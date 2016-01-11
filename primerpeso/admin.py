from django.contrib import admin
from primerpeso import models, forms


@admin.register(models.Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
	form = forms.OpportunityForm

admin.site.register(models.Requirement)
admin.site.register(models.Agency)
