from . import models
from .serializers import OpportunitySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny


class OpportunityLCAPI(ListCreateAPIView):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = (AllowAny,)


class OpportunityRAPI(RetrieveAPIView):
    pass
