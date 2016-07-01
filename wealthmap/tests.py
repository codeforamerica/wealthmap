from django.conf import settings
from django.contrib.auth import models as auth_models
from django.test import Client, TestCase, override_settings
from .serializers import OpportunitySerializer
from . import models


@override_settings(WEALTHMAP_SEARCHABLE_OPPORTUNITY={
    'app_label': 'wealthmap',
    'model_name': 'ExampleOpportunity',
})
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

    def test_create_api_uses_settings(self):
        """Test that the create API endpoint uses the model defined in
        settings.WEALTHMAP_SEARCHABLE_OPPORTUNITY"""

        self.assertEqual(
            OpportunitySerializer.Meta.model, models.ExampleOpportunity)

# This override isn't actually used below
# But is included because Django is confused if settings change during testing


@override_settings(WEALTHMAP_SEARCHABLE_OPPORTUNITY={
    'app_label': 'wealthmap',
    'model_name': 'ExampleOpportunity',
})
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
        self.purpose_a = models.Purpose.objects.create(
            name='Hiring', creator=self.user)
        self.purpose_b = models.Purpose.objects.create(
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
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_a.industries.add(self.industry_manuf)
        opportunity_b = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_b.industries.add(self.industry_agri)
        opportunity_c = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="C")})

        new_industry = {'industry': self.industry_manuf}
        opp_search = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **new_industry},
        )

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 2)
        self.assertEqual(result_set[0], opportunity_a)
        self.assertEqual(result_set[1], opportunity_c)

    def test_opportunity_search_with_purpose(self):
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_a.purposes.add(self.purpose_a)
        opportunity_b = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_b.purposes.add(self.purpose_b)

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)
        opp_search.purposes.add(self.purpose_a)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 1)
        self.assertEqual(result_set[0], opportunity_a)

    def test_opportunity_search_when_no_industry(self):
        """
        If nothing is searched for, only give Opportunities without industry.
        `null` is effectively the same as "Other"
        """
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_a.industries.add(self.industry_manuf)
        opportunity_b = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 1)
        self.assertEqual(result_set[0], opportunity_b)

    def test_opportunity_search_when_no_purpose(self):
        """
        If nothing is searched for, return all Opportunities
        TODO: Could this be more specific? Check back on user data in a year.
        """
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_a.purposes.add(self.purpose_a)
        opportunity_b = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})

        opp_search = models.OpportunitySearch.objects.create(
            **self.opp_search_base)

        result_set = opp_search.search()
        self.assertEqual(result_set.count(), 2)

    def test_opportunity_search_with_personal_investment(self):
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A", personal_investment=True)})
        opportunity_b = models.ExampleOpportunity.objects.create(
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
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base,
               **dict(title="A", existing_business='existing')})
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B", existing_business='new')})
        models.ExampleOpportunity.objects.create(
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
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A", small_business=True)})
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B", small_business=False)})

        # Return *only* Opps with `False` when user has a large business
        opp_search_A = models.OpportunitySearch.objects.create(
            **{**self.opp_search_base, **{'small_business': False}})

        result_set_A = opp_search_A.search()
        self.assertEqual(result_set_A.count(), 1)

        # Return *all* Opps when user is small business (True)
        query_dict = {**self.opp_search_base, **{'small_business': True}}
        opp_search_B = models.OpportunitySearch.objects.create(**query_dict)

        result_set_B = opp_search_B.search()
        self.assertEqual(result_set_B.count(), 2)

    def test_opportunity_search_create_endpoint(self):
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A", small_business=True)})
        models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B", small_business=False)})

        client = Client()
        response = client.post('/wm-api/search/', {
            **{**self.opp_search_base, **{'small_business': False}}
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['results']), 1)

    def test_opportunity_search_create_endpoint_with_purposes(self):
        opportunity_a = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="A")})
        opportunity_a.purposes.add(self.purpose_a)
        opportunity_b = models.ExampleOpportunity.objects.create(
            **{**self.opp_base, **dict(title="B")})
        opportunity_b.purposes.add(self.purpose_b)

        client = Client()
        query_dict = self.opp_search_base
        query_dict['purposes'] = [self.purpose_a.pk, ]
        response = client.post('/wm-api/search/', query_dict)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['results']), 1)
