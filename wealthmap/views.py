from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .serializers import OpportunitySerializer, OpportunitySearchSerializer
from . import models


class OpportunityRAPI(RetrieveAPIView):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = (AllowAny,)


# class SearchCAPI(CreateAPIView):
#     queryset = models.OpportunitySearch.objects.all()
#     serializer_class = OpportunitySearchSerializer
#     permission_classes = (AllowAny,)

#     # Override default method to return search results instead of search
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)

#         return Response(serializer.data,
#             status=status.HTTP_201_CREATED, headers=headers)


class SearchRAPI(RetrieveAPIView):

    """This view should return JSON for every Opportunity that fits
    the search criteria."""

    serializer_class = OpportunitySearchSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        import pdb
        pdb.set_trace()
