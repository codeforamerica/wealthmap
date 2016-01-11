from django import forms
from primerpeso import models

from primerpeso.widgets import ArrayFieldSelectMultiple


class OpportunityForm(forms.ModelForm):

    class Meta:
        model = models.Opportunity
        exclude = ['creator']
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
