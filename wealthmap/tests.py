from django.conf import settings
from django.db import models
from django.test import TestCase, override_settings
from .models import Opportunity, ExampleOpportunity


@override_settings(WEALTHMAP_SEARCHABLE_OPPORTUNITY=ExampleOpportunity)
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
            self.OpportunitySerializer.Meta.model, ExampleOpportunity)
