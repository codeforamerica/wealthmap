from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import *
from . import forms, models


class OpportunitySearchCreateView(CreateView):
        model = models.OpportunitySearch
        form_class = forms.OpportunitySearchForm
        template_name = 'wealthmap/opportunity_search_form.html'


class OpportunityDetailView(DetailView):
        model = models.get_search_model()
        template_name = 'wealthmap/opportunity_detail.html'


class OpportunityListView(ListView):
        model = models.get_search_model()
        template_name = 'wealthmap/opportunity_list.html'


class OpportunitySearchDetailView(DetailView):
        model = models.OpportunitySearch
        template_name = 'wealthmap/opportunity_search_detail.html'


class OpportunityRAPI(RetrieveAPIView):
    queryset = models.get_search_model().objects.all()
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


class BenefitTypeLAPI(ListAPIView):
    queryset = models.BenefitType.objects.all()
    serializer_class = BenefitTypeSerializer
    permission_classes = (AllowAny,)


class BenefitTypeRAPI(RetrieveAPIView):
    queryset = models.BenefitType.objects.all()
    serializer_class = BenefitTypeSerializer
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
