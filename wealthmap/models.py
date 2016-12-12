from django.apps import apps
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField, USZipCodeField
from localflavor.us.models import PhoneNumberField


class WhenBase(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Last Modified'))

    class Meta:
        abstract = True


class WhoAndWhenBase(WhenBase):

    """An abstract base class which manages created at and updated at as well
    as who created it.
    """
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'))

    class Meta:
        abstract = True


class Industry(WhoAndWhenBase):
    name = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('order',)
        verbose_name = _('Industry')
        verbose_name_plural = _('Industries')


class Purpose(WhoAndWhenBase):
    name = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('order',)


class BenefitType(WhoAndWhenBase):
    name = models.CharField(max_length=32)
    order = models.PositiveSmallIntegerField(
        default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('order',)


class AgencyProvider(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Agency(WhoAndWhenBase):

    """A government or other entity that Opportunities belong to.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'))
    phone = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('phone'))
    fax = models.CharField(blank=True, max_length=255, verbose_name=_('fax'))
    email = models.EmailField(blank=True, verbose_name=_('email'))
    street_address = models.TextField(blank=True,
                                      verbose_name=_('street address'))
    url = models.URLField(max_length=255, blank=True, verbose_name=_('url'))
    provider = models.ForeignKey(AgencyProvider, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')


BENEFIT_TYPE_CHOICES = (
    ('money', _('money')),
    ('advice', _('advice')),
)

EXISTING_BUSINESS_CHOICES = (
    ('existing', _('existing business')),
    ('new', _('new business')),
    ('', _('either')),
)


class Opportunity(WhoAndWhenBase):

    """A government sponsored incentive/grant/tax break for businesses.
    These fields represent the properties of a business that would
    be eligible or well-suited for a particular opportunity.
    """

    title = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_('title'))

    benefit_types = models.ManyToManyField(
        BenefitType,
        blank=True,
        verbose_name=_('benefit types'))
    # Industry options: [manufacturing, finance, agriculture, other]
    industries = models.ManyToManyField(
        Industry,
        blank=True,
        verbose_name=_('industries'))
    personal_investment = models.BooleanField(
        verbose_name=_('requires personal investment'))
    existing_business = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        choices=EXISTING_BUSINESS_CHOICES,
        verbose_name=_('this opportunity applies to'))
    small_business = models.BooleanField(
        verbose_name=_('must be a small business'))
    purposes = models.ManyToManyField(
        Purpose,
        blank=True,
        verbose_name=_('purposes'),
        help_text=_('leave blank if none apply'))
    agency = models.ForeignKey(Agency, verbose_name=_('agency'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Opportunity')
        verbose_name_plural = _('Opportunities')


class ExampleOpportunity(Opportunity):

    """Subclassed Opportunity model used as an example
    and for writing test cases."""
    description = models.TextField()


class OpportunitySearch(WhenBase):

    """Represents a particular user search. Useful for saving past searches,
    providing analytics, etc."""
    industries = models.ManyToManyField(
        Industry,
        verbose_name=_('What type of business are you?'))
    personal_investment = models.BooleanField(
        verbose_name=_('Are you investing personal money?'))

    existing_business = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        choices=EXISTING_BUSINESS_CHOICES,
        verbose_name=_('What stage are you at?'))
    small_business = models.BooleanField(
        verbose_name=_('Are you a small business?'))
    purposes = models.ManyToManyField(
        Purpose,
        verbose_name=_('What are you looking for?'))
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Opportunity Search %d' % self.pk

    class Meta:
        verbose_name = _('Opportunity Search')
        verbose_name_plural = _('Opportunity Searches')

    def get_absolute_url(self):
        return reverse('wealthmap:opportunity-search-detail', args=(self.pk,))

    def search(self):
        opps = get_search_model().objects

        # If nothing is searched for, only give Opportunities without industry.
        # `null` is effectively the same as "Other"
        if self.industries.count() > 0:
            opps = opps.filter(
                Q(industries__in=self.industries.all()) |
                Q(industries__isnull=True))
        else:
            opps = opps.filter(industries__isnull=True)

        # only filter by personal_investment if `False`
        # if `True`, just return all Opps to the user
        if not self.personal_investment:
            opps = opps.filter(personal_investment=self.personal_investment)

        if self.existing_business:
            opps = opps.filter(existing_business=self.existing_business)

        # only filter by small_business if `False`
        # if `True`, just return all Opps to the user
        if not self.small_business:
            opps = opps.filter(small_business=self.small_business)

        if self.purposes.count() > 0:
            opps = opps.filter(purposes__in=self.purposes.all())

        # opps with multiple purposes, industries, etc.
        # may show up multiple times due to joins
        opps = opps.distinct()
        self.view_count += 1
        self.save()
        return opps


def get_search_model():
    '''
    Serializer shouldn't be defined unless settings are present
    This situation arises when testing, as tests shouldn't depend
    on the environment in which the code is running.
    '''
    # TODO: Set ExampleOpportunity as default in app settings.
    if hasattr(settings, 'WEALTHMAP_SEARCHABLE_OPPORTUNITY'):
        search_model = apps.get_model(
            **settings.WEALTHMAP_SEARCHABLE_OPPORTUNITY)
    else:
        search_model = ExampleOpportunity

    return search_model
