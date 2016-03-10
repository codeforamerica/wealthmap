from django import forms
from primerpeso import models

from primerpeso.widgets import ArrayFieldSelectMultiple


class OpportunitySearchForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.OpportunitySearch
        widgets = {
            "purpose": ArrayFieldSelectMultiple(
                choices=models.PURPOSE, attrs={'class': 'chosen'}),
            "locations": ArrayFieldSelectMultiple(
                choices=models.LOCATIONS, attrs={'class': 'chosen'}),
        }


class PurposeSearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['email', 'purpose', 'investing_own_money']
        widgets = {
            "purpose": ArrayFieldSelectMultiple(
                choices=models.PURPOSE, attrs={'class': 'chosen'}),
        }


class AboutSearchForm(forms.ModelForm):

    class Meta:
        model = models.OpportunitySearch
        fields = ['gender', 'age']


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


class OpportunityForm(forms.ModelForm):

    class Meta:
        model = models.Opportunity
        exclude = []
        widgets = {
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
