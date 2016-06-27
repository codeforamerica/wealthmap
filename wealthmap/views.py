from . import models
from .serializers import OpportunitySerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny


class OpportunityRAPI(RetrieveAPIView):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = (AllowAny,)
