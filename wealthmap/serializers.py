from django.apps import apps
from django.conf import settings
from rest_framework import serializers
from . import models


class BenefitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BenefitType
        exclude = ('creator',)


class IndustrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Industry
        exclude = ('creator',)


class PurposeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Purpose
        exclude = ('creator',)


class OpportunitySerializer(serializers.ModelSerializer):
    benefit_types = BenefitTypeSerializer
    industries = IndustrySerializer
    purposes = PurposeSerializer

    class Meta:
        model = models.get_search_model()
        exclude = ('creator',)
        depth = 1


class OpportunitySearchSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()
    benefit_types = serializers.PrimaryKeyRelatedField(
        queryset=models.BenefitType.objects.all(), many=True)
    industries = serializers.PrimaryKeyRelatedField(
        queryset=models.Industry.objects.all(), many=True)
    purposes = serializers.PrimaryKeyRelatedField(
        queryset=models.Purpose.objects.all(), many=True)

    def get_results(self, obj):
        serializer = OpportunitySerializer(obj.search(), many=True)
        return serializer.data

    def create(self, validated_data):
        benefit_types = validated_data.pop('benefit_types')
        purposes = validated_data.pop('purposes')
        industries = validated_data.pop('industries')

        obj = models.OpportunitySearch.objects.create(**validated_data)

        if benefit_types:
            obj.benefit_types.add(*benefit_types)
        if purposes:
            obj.purposes.add(*purposes)
        if industries:
            obj.industries.add(*industries)

        return obj

    class Meta:
        model = models.OpportunitySearch
        exclude = ()
        depth = 1
