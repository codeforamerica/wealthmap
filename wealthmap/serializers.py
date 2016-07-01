from django.apps import apps
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
    search_model = apps.get_model(**settings.WEALTHMAP_SEARCHABLE_OPPORTUNITY)
else:
    search_model = models.ExampleOpportunity


class IndustrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Industry
        exclude = ('creator',)


class PurposeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Purpose
        exclude = ('creator',)


class OpportunitySerializer(serializers.ModelSerializer):
    industries = IndustrySerializer
    purposes = PurposeSerializer

    class Meta:
        model = search_model
        exclude = ('creator',)
        depth = 1


class OpportunitySearchSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    purposes = serializers.PrimaryKeyRelatedField(
        queryset=models.Purpose.objects.all(), many=True)

    def get_results(self, obj):
        # TODO: Dirty way to get valid JSON.
        # Should actually use OpportunitySerializer somehow
        serializer = OpportunitySerializer(obj.search(), many=True)
        return serializer.data

    def create(self, validated_data):
        purposes = validated_data.pop('purposes')
        obj = models.OpportunitySearch.objects.create(**validated_data)
        if purposes:
            obj.purposes.add(*purposes)
        return obj

    class Meta:
        model = models.OpportunitySearch
        exclude = ()
        depth = 1
