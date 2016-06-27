from django.conf import settings
from rest_framework import serializers
from . import models

'''
Serializer shouldn't be defined unless settings are present
This situation arises when testing, as tests shouldn't depend
on the environment in which the code is running.
'''
# TODO: Set ExampleOpportunity as default in app settings.
if hasattr(settings, 'WEALTHMAP_SEARCHABLE_OPPORTUNITY'):
    search_model = settings.WEALTHMAP_SEARCHABLE_OPPORTUNITY
else:
    search_model = models.Opportunity


class OpportunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = search_model
        exclude = ('creator')
