from django import forms
from wealthmap import models
from django.utils.translation import ugettext as _
from wealthmap.widgets import ArrayFieldSelectMultiple


class OpportunityListForm(forms.Form):
    opportunities = forms.ModelMultipleChoiceField(
        queryset=models.Opportunity.objects.all())


class OpportunitySearchForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = models.OpportunitySearch


class OpportunityForm(forms.ModelForm):

    class Meta:
        model = models.Opportunity
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }


class BenefitTypeForm(forms.ModelForm):

    class Meta:
        model = models.BenefitType
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }


class AgencyForm(forms.ModelForm):

    class Meta:
        model = models.Agency
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }


class IndustryForm(forms.ModelForm):

    class Meta:
        model = models.Industry
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }


class PurposeForm(forms.ModelForm):

    class Meta:
        model = models.Purpose
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }
