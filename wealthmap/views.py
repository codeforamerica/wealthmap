from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .serializers import OpportunitySerializer, OpportunitySearchSerializer
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
