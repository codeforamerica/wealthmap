from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import *
from . import models


class OpportunityRAPI(RetrieveAPIView):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = (AllowAny,)


class SearchCAPI(CreateAPIView):
    queryset = models.OpportunitySearch.objects.all()
    serializer_class = OpportunitySearchSerializer
    permission_classes = (AllowAny,)


class SearchRAPI(RetrieveAPIView):

    """This view should return JSON for every Opportunity that fits
    the search criteria."""

    queryset = models.OpportunitySearch.objects.all()
    serializer_class = OpportunitySearchSerializer
    permission_classes = (AllowAny,)


class IndustryLAPI(ListAPIView):
    queryset = models.Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = (AllowAny,)


class IndustryRAPI(RetrieveAPIView):
    queryset = models.Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = (AllowAny,)


class PurposeLAPI(ListAPIView):
    queryset = models.Purpose.objects.all()
    serializer_class = PurposeSerializer
    permission_classes = (AllowAny,)


class PurposeRAPI(RetrieveAPIView):
    queryset = models.Purpose.objects.all()
    serializer_class = PurposeSerializer
    permission_classes = (AllowAny,)
