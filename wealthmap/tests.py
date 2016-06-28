from django.conf import settings
from django.contrib.auth import models as auth_models
from django.test import TestCase, override_settings
from . import models


@override_settings(WEALTHMAP_SEARCHABLE_OPPORTUNITY=models.ExampleOpportunity)
class OpportunityTestCase(TestCase):

    """
    Tests to demonstrate that the API uses the proper Opportunity subclass
    specified by settings.
    """

    def setUp(self):
        """
        Serializer is loaded *after* the app is initialized
        so that settings can be overridden first (see @override_settings).
        """
        from .serializers import OpportunitySerializer as OppSerializer
        # This line is a hack because self.X can't be assigned in an import
        # TODO: There must be a better way to do this.
        self.OpportunitySerializer = OppSerializer

    def test_create_api_uses_settings(self):
        """Test that the create API endpoint uses the model defined in
        settings.WEALTHMAP_SEARCHABLE_OPPORTUNITY"""

        self.assertEqual(
            self.OpportunitySerializer.Meta.model, models.ExampleOpportunity)


class OpportunitySearchTestCase(TestCase):

    """
    Tests for the creating and viewing instances of OpportunitySearch model.
    """

    def setUp(self):
        self.user = auth_models.User.objects.create(
            username='A', password='B')
        self.industry_A = models.Industry.objects.create(
            name='Manufacturing', creator=self.user)
        self.industry_B = models.Industry.objects.create(
            name='Agriculture', creator=self.user)
        self.purpose_A = models.Purpose.objects.create(
            name='Hiring', creator=self.user)
        self.purpose_B = models.Purpose.objects.create(
            name='Construction', creator=self.user)

        self.opp_base = dict(
            city='Long Beach',
            state='CA',
            personal_investment=True,
            existing_business='new',
            small_business=True,
            creator=self.user,
        )

        self.opp_search_base = dict(
            city='Long Beach',
            state='CA',
            personal_investment=True,
            existing_business='new',
            small_business=True,
        )

    def test_view_count_increments(self):
        """Test that saving an existing search model increments the counter
        by one."""
        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        self.assertEqual(opp_search.view_count, 1)
        opp_search.save()
        self.assertEqual(opp_search.view_count, 2)

    def test_opportunity_search_with_industry(self):
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_A.industries.add(self.industry_A)
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_B.industries.add(self.industry_B)

        new_industry = {'industry': self.industry_A}
        opp_search = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **new_industry},
        )

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 1)
        self.assertEqual(result_set[0], opportunity_A)

    def test_opportunity_search_with_purpose(self):
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_A.purposes.add(self.purpose_A)
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_B.purposes.add(self.purpose_B)

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)
        opp_search.purposes.add(self.purpose_A)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 1)
        self.assertEqual(result_set[0], opportunity_A)

    def test_opportunity_search_when_no_industry(self):
        # TODO: `null` is effectively the same as "Other"
        # If nothing is searched for, only give Opportunities without industry
        raise NotImplemetedError

    def test_opportunity_search_when_no_purpose(self):
        raise NotImplemetedError
