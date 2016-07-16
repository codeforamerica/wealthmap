from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from wealthmap import models, forms


class AddCreatorMixin:

    def get_form(self, request, *args, **kwargs):
        form = super(AddCreatorMixin, self).get_form(request, *args, **kwargs)
        form.base_fields['creator'].initial = request.user
        return form


class AddCreator(AddCreatorMixin, admin.ModelAdmin):

    """Subclass of ``ModelAdmin``s which adds the user to the creator field.
    """
    pass


@admin.register(models.Agency)
class AgencyAdmin(AddCreator):
    form = forms.AgencyForm


@admin.register(models.Opportunity)
class OpportunityAdmin(AddCreator):
    form = forms.OpportunityForm


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


class SortableAdmin(SortableAdminMixin, AddCreator):
    pass


@admin.register(models.BenefitType)
class BenefitTypeAdmin(SortableAdmin):
    form = forms.BenefitTypeForm


@admin.register(models.Purpose)
class PurposeAdmin(SortableAdmin):
    form = forms.PurposeForm


@admin.register(models.Industry)
class IndustryAdmin(SortableAdmin):
    form = forms.IndustryForm
