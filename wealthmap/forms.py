from django import forms
from wealthmap import models
from django.utils.translation import ugettext as _
from wealthmap.widgets import ArrayFieldSelectMultiple


class OpportunityListForm(forms.Form):
    opportunities = forms.ModelMultipleChoiceField(
        queryset=models.Opportunity.objects.all())

'''
class OpportunitySearchForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = models.OpportunitySearch
        widgets = {
            "purpose": ArrayFieldSelectMultiple(
                choices=models.PURPOSE_SEARCH, attrs={'class': 'chosen'}),
            "locations": ArrayFieldSelectMultiple(
                choices=models.LOCATIONS_SEARCH, attrs={'class': 'chosen'}),
        }


class PurposeSearchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PurposeSearchForm, self).__init__(*args, **kwargs)
        self.fields['investing_own_money'].required = True

    class Meta:
        model = models.OpportunitySearch

        fields = ['purpose', 'investing_own_money']

        widgets = {
            "purpose": ArrayFieldSelectMultiple(
                choices=models.PURPOSE_SEARCH, attrs={'class': 'chosen'}),
            "investing_own_money": forms.RadioSelect(choices=models.YES_NO)
        }


class AboutSearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['gender', ]


class IndustrySearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['entity_type', 'industry']


class LocationSearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['locations']
        widgets = {
            "locations": ArrayFieldSelectMultiple(
                choices=models.LOCATIONS, attrs={'class': 'chosen'}),
        }


class SizeSearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['employees', 'years_in_business', 'annual_revenue']
'''

class OpportunityForm(forms.ModelForm):

    class Meta:
        model = models.Opportunity
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
        }
