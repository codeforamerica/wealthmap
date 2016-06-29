from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
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


EXISTING_BUSINESS_CHOICES = (
    ('existing', _('existing business')),
    ('new', _('new business')))


class Opportunity(WhoAndWhenBase):

    """A government sponsored incentive/grant/tax break for businesses.
    These fields represent the properties of a business that would
    be eligible or well-suited for a particular opportunity.
    """
    city = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=_('city'))
    state = USStateField(verbose_name=_('state'))
    # Industry options: [manufacturing, finance, agriculture, other]
    industries = models.ManyToManyField(
        Industry,
        blank=True,
        verbose_name=_('industries'))
    personal_investment = models.BooleanField(
        verbose_name=_('personal investment'))
    existing_business = models.CharField(max_length=8,
                                         null=True,
                                         blank=True,
                                         choices=EXISTING_BUSINESS_CHOICES,
                                         verbose_name=_('existing business'))
    small_business = models.BooleanField(
        verbose_name=_('small business'))
    # Purpose options:
    #   - equipment purchase
    #   - construction/remodel
    #   - hiring
    #   - training
    #   - disaster recovery
    #   - relocating
    #   - out of state sales
    purposes = models.ManyToManyField(
        Purpose,
        blank=True,
        verbose_name=_('purposes'))

    title = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_('title'))

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
    city = models.CharField(max_length=255, verbose_name=_('city'))
    state = USStateField(verbose_name=_('state'))
    # Industry options: [manufacturing, finance, agriculture, other]
    industry = models.ForeignKey(
        Industry,
        null=True,
        blank=True,
        verbose_name=_('industries'))
    personal_investment = models.BooleanField(
        verbose_name=_('personal investment'))

    existing_business = models.CharField(max_length=8,
                                         choices=EXISTING_BUSINESS_CHOICES,
                                         verbose_name=_('existing business'))
    small_business = models.BooleanField(
        verbose_name=_('small business'))
    # Purpose options:
    #   - equipment purchase
    #   - construction/remodel
    #   - hiring
    #   - training
    #   - disaster recovery
    #   - relocating
    #   - out of state sales
    purposes = models.ManyToManyField(
        Purpose,
        verbose_name=_('purposes'))
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.view_count += 1
        return super(OpportunitySearch, self).save(*args, **kwargs)

    def __str__(self):
        return 'Opportunity Search %d' % self.pk

    class Meta:
        verbose_name = _('Opportunity Search')
        verbose_name_plural = _('Opportunity Searches')

    def search(self):
        opps = Opportunity.objects.filter(
            city__iexact=self.city).filter(
            state=self.state)

        if self.industry:
            opps = opps.filter(
                Q(industries=self.industry) | Q(industries__isnull=True))
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

        return opps


'''
class OpportunitySearch(models.Model):

    def search(self):
        opps = Opportunity.objects

        def min_max_query(query, field_name, value):
            """
            modifies a query so if finds Opportunities which match searches.
            """
            min_query = {field_name + '_min__lte': value}
            max_query = {field_name + '_max__gte': value}
            no_max = {field_name + '_max__isnull': True}
            return query.filter(
                Q(**min_query) & Q(Q(**max_query) | Q(**no_max)))

        def make_contains(field_name, search_term):
            query_str = '%s__contains' % field_name
            return Q(**{query_str: [search_term, ]})

        def multi_select(field_name, select):
            q = make_contains(field_name, 'any')
            for s in select:
                q |= make_contains(field_name, s)
            return q

        opps = opps.filter(multi_select('purpose', self.purpose))
        if not self.investing_own_money:
            opps = opps.filter(investing_own_money=False)
        genders = ['any']
        if self.gender == 'both':
            genders.extend(['male', 'female'])
        else:
            genders.append(self.gender)
        opps = opps.filter(gender__in=genders)
        opps = opps.filter(multi_select('entity_types', [self.entity_type, ]))
        opps = opps.filter(multi_select('industries', [self.industry, ]))
        opps = opps.filter(multi_select('locations', self.locations))
        opps = min_max_query(opps, 'employees', self.employees)
        opps = opps.filter(
            minimum_years_in_business__lte=self.years_in_business)
        opps = min_max_query(opps, 'annual_revenue', self.annual_revenue)
        opps = opps.order_by('title')
        return opps

    def segment_search(self):
        results = self.search()
        opps_by_type = {
            key: {'name': value, 'opps': []} for (key, value) in BENEFIT_TYPES}
        for result in results:
            for benefit_type in result.benefit_types:
                opps_by_type[benefit_type]['opps'].append(result)
        return opps_by_type

    def __str__(self):
        return 'Search: %s' % self.pk

    class Meta:
        verbose_name = _('Opportunity Search')
        verbose_name_plural = _('Opportunity Searches')


class Contact(models.Model):
    """The contact information added to a search so that Agencies
    get an email.
    """
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Contact Date and Time'))
    full_name = models.CharField(max_length=255,
                                 verbose_name=_('Full Name'))
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'))
    email = models.EmailField(verbose_name=_('Email'))
    address = models.CharField(max_length=255,
                               verbose_name=_('Postal Address'))
    city = models.CharField(max_length=255,
                            verbose_name=_('City / Town'))
    state = USStateField(verbose_name=_('State or Province'))
    postal_code = USZipCodeField(verbose_name=_('Postal Code'))
    incorporated = models.BooleanField(
        verbose_name=_('Are You Incorporated?'),
        choices=YES_NO,
        blank=False,
        default=False,
    )
    company = models.CharField(max_length=255,
                               verbose_name=_('Legal Business Name'))
    company_municipality = models.CharField(
        max_length=255,
        verbose_name=_('Company Municipality')
    )
    company_state = USStateField(verbose_name=_('Company State or Province'))
    company_postal_code = USZipCodeField(verbose_name=_('Company Postal Code'))
    search = models.ForeignKey(OpportunitySearch,
                               verbose_name=_('Related Search'))
    opportunities = models.ManyToManyField(
        Opportunity,
        verbose_name=_('Related Opportunities')
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Search Contact')
        verbose_name_plural = _('Search Contacts')
'''
