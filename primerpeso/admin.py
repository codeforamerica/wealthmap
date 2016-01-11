from django.contrib import admin
from primerpeso import models, forms


class AddCreator:
	"""A mixin for ``ModelAdmin``s which adds the user to the creator field.
	"""
	def get_form(self, request, *args, **kwargs):
		form = super(PageAdmin, self).get_form(request, *args, **kwargs)
		form.base_fields['creator'].initial = request.user
		return form

@admin.register(models.Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    form = forms.OpportunityForm


admin.site.register(models.Requirement)
admin.site.register(models.Agency)
