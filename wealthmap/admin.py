from django.contrib import admin
from wealthmap import models, forms


class AddCreatorMixin:
    """Subclass of ``ModelAdmin``s which adds the user to the creator field.
    """

    def get_form(self, request, *args, **kwargs):
        form = super(AddCreator, self).get_form(request, *args, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form


class AddCreator(admin.ModelAdmin, AddCreatorMixin):
    pass


class AddCreatorInline(admin.StackedInline, AddCreatorMixin):
    pass


class RequirementInlineAdmin(AddCreatorInline):
    form = forms.RequirementForm
    model = models.Requirement


class RequirementRelationshipAdmin(AddCreatorInline):
    form = forms.RequirementRelationshipForm
    model = models.RequirementRelationship
    extra = 1
    inlines = (RequirementInlineAdmin, )


@admin.register(models.Opportunity)
class OpportunityAdmin(AddCreator):
    form = forms.OpportunityForm
    inlines = (RequirementRelationshipAdmin, )


@admin.register(models.Requirement)
class RequirementAdmin(AddCreator):
    form = forms.RequirementForm


@admin.register(models.OpportunitySearch)
class OpportunitySearchAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(OpportunitySearchAdmin,
                     self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Agency)
class AgencyAdmin(AddCreator):
    form = forms.RequirementForm

admin.site.register(models.Contact)
