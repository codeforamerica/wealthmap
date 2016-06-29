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
        self.industry_manuf = models.Industry.objects.create(
            name='Manufacturing', creator=self.user)
        self.industry_agri = models.Industry.objects.create(
            name='Agriculture', creator=self.user)
        self.purpose_A = models.Purpose.objects.create(
            name='Hiring', creator=self.user)
        self.purpose_B = models.Purpose.objects.create(
            name='Construction', creator=self.user)

        self.opp_base = dict(
            city='Long Beach',
            state='CA',
            personal_investment=True,
            small_business=True,
            creator=self.user,
        )

        self.opp_search_base = dict(
            city='Long Beach',
            state='CA',
            personal_investment=True,
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
        # Should return Opps with appropriate industry *or* `null` industry
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_A.industries.add(self.industry_manuf)
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_B.industries.add(self.industry_agri)
        opportunity_C = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="C")})

        new_industry = {'industry': self.industry_manuf}
        opp_search = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **new_industry},
        )

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 2)
        self.assertEqual(result_set[0], opportunity_A)
        self.assertEqual(result_set[1], opportunity_C)

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
        """
        If nothing is searched for, only give Opportunities without industry.
        `null` is effectively the same as "Other"
        """
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_A.industries.add(self.industry_manuf)
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 1)
        self.assertEqual(result_set[0], opportunity_B)

    def test_opportunity_search_when_no_purpose(self):
        """
        If nothing is searched for, return all Opportunities
        TODO: Could this be more specific? Check back on user data in a year.
        """
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_A.purposes.add(self.purpose_A)
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 2)

    def test_opportunity_search_with_personal_investment(self):
        opportunity_A = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A", personal_investment=True)})
        opportunity_B = models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B", personal_investment=False)})

        # Return *only* Opps with `False` if user is not investing (False)
        opp_search_A = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'personal_investment': False}})

        result_set_A = opp_search_A.search()
        self.assertEqual(result_set_A.count(), 1)

        # Return *all* Opps when user is investing (True)
        opp_search_B = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'personal_investment': True}})

        result_set_B = opp_search_B.search()
        self.assertEqual(result_set_B.count(), 2)

    def test_opportunity_search_with_existing_business(self):
        models.Opportunity.objects.create(
            **{**self.opp_base,
               **dict(title="A", existing_business='existing')})
        models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B", existing_business='new')})
        models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="C")})

        # Return *only* Opps with relevant value when specified
        opp_search_A = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'existing_business': 'existing'}})

        result_set_A = opp_search_A.search()
        self.assertEqual(result_set_A.count(), 1)

        # Return *all* Opps when no value is specified
        opp_search_B = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        result_set_B = opp_search_B.search()
        self.assertEqual(result_set_B.count(), 3)

    def test_opportunity_search_with_small_business(self):
        models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="A", small_business=True)})
        models.Opportunity.objects.create(
            **{**self.opp_base, **dict(title="B", small_business=False)})

        # Return *only* Opps with `False` when user has a large business
        opp_search_A = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'small_business': False}})

        result_set_A = opp_search_A.search()
        self.assertEqual(result_set_A.count(), 1)

        # Return *all* Opps when user is small business (True)
        opp_search_B = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'small_business': True}})

        result_set_B = opp_search_B.search()
        self.assertEqual(result_set_B.count(), 2)
