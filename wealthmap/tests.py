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
        self.industry = models.Industry.objects.create(
            name='Manufacturing', creator=self.user)
        self.purpose = models.Purpose.objects.create(
            name='Hiring', creator=self.user)

    def test_view_count_increments(self):
        """Test that saving an existing search model increments the counter
        by one."""

        search = models.OpportunitySearch.objects.create(
            city='Long Beach',
            state='CA',
            personal_investment=True,
            existing_business='new',
            small_business=True,
        )

        self.assertEqual(search.view_count, 1)
        search.save()
        self.assertEqual(search.view_count, 2)
