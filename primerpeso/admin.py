from django.contrib import admin
from primerpeso import models, forms


class AddCreator(admin.ModelAdmin):
    """Subclass of ``ModelAdmin``s which adds the user to the creator field.
    """

    def get_form(self, request, *args, **kwargs):
        form = super(AddCreator, self).get_form(request, *args, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form


@admin.register(models.Opportunity)
class OpportunityAdmin(AddCreator):
    form = forms.OpportunityForm


@admin.register(models.Requirement)
class RequirementAdmin(AddCreator):
    pass


@admin.register(models.Agency)
class AgencyAdmin(AddCreator):
    pass
