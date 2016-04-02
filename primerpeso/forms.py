from django import forms
from primerpeso import models
from django.utils.translation import ugettext as _
from primerpeso.widgets import ArrayFieldSelectMultiple


class PersonalContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonalContactForm, self).__init__(*args, **kwargs)
        self.fields['incorporated'].required = True

    class Meta:
        fields = ['full_name', 'phone_number', 'email', 'address', 'city',
                  'state', 'postal_code', 'incorporated', ]
        model = models.Contact
        widgets = {
            "incorporated": forms.RadioSelect(choices=models.YES_NO)
        }


class BusinessContactForm(forms.ModelForm):

    class Meta:
        fields = ['company', 'company_municipality', 'company_state',
                  'company_postal_code', ]
        model = models.Contact


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


class AgencyForm(forms.ModelForm):

    class Meta:
        widgets = {
            "creator": forms.HiddenInput(),
        }


class RequirementRelationshipForm(forms.ModelForm):

    class Meta:
        widgets = {
            "creator": forms.HiddenInput(),
        }


class RequirementForm(forms.ModelForm):

    class Meta:
        widgets = {
            "creator": forms.HiddenInput(),
        }


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = models.Opportunity
        exclude = []
        widgets = {
            "creator": forms.HiddenInput(),
            "locations": ArrayFieldSelectMultiple(
                choices=models.LOCATIONS, attrs={'class': 'chosen'}),
            "entity_types": ArrayFieldSelectMultiple(
                choices=models.ENTITY_TYPES, attrs={'class': 'chosen'}),
            "industries": ArrayFieldSelectMultiple(
                choices=models.INDUSTRIES, attrs={'class': 'chosen'}),
            "demographics": ArrayFieldSelectMultiple(
                choices=models.DEMOGRAPHICS, attrs={'class': 'chosen'}),
            "benefit_types": ArrayFieldSelectMultiple(
                choices=models.BENEFIT_TYPES, attrs={'class': 'chosen'}),
            "purpose": ArrayFieldSelectMultiple(
                choices=models.PURPOSE, attrs={'class': 'chosen'}),
        }
"""
    class Media:
        css = {
            "all": ("chosen/chosen.min.css", )
        }
        js = ("js/jquery.min.js", "chosen/chosen.jquery.min.js")
"""
