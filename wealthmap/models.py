from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField, USZipCodeField
from localflavor.us.models import PhoneNumberField


class WhoAndWhenBase(models.Model):

    """An abstract base class which manages created at and updated at as well
    as who created it.
    """
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Made On'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Last Modified'))
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'))

    class Meta:
        abstract = True


class Industry(WhoAndWhenBase):
    name = models.CharField(max_length=32)


class Purpose(WhoAndWhenBase):
    name = models.CharField(max_length=32)


PURPOSE = (
    ('any', 'Any'),  # should be any
)

PURPOSE_SEARCH = PURPOSE[1:]  # excludes the first 'any' option


class Opportunity(WhoAndWhenBase):

    """A government sponsored incentive/grant/tax break for businesses.
    These fields represent the properties of a business that would
    be eligible or well-suited for a particular opportunity.
    """
    city = models.CharField(max_length=255, verbose_name=_('city'))
    state = USStateField(verbose_name=_('state'))
    # Industry options: [manufacturing, finance, agriculture, other]
    industries = models.ManyToManyField(
        Industry,
        verbose_name=_('industries'))
    personal_investment = models.BooleanField(
        verbose_name=_('personal investment'))
    existing_business = models.CharField(max_length=8,
                                         null=True,
                                         blank=True,
                                         choices=(
                                             ('existing',
                                              _('existing business')),
                                             ('new', _('new business'))),
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
    purpose = models.ManyToManyField(
        Purpose,
        verbose_name=_('purpose'))

    title = models.CharField(
        max_length=255,
        unique=True,
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


'''
class OpportunitySearch(models.Model):
    """Is created every time a new search is run and contains all
    the search options.
    """
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Search Date and Time'))
    purpose = ArrayField(
        models.CharField(max_length=255, choices=PURPOSE_SEARCH),
        default=list, verbose_name=_('How would you use the incentive?'),
    )
    investing_own_money = models.BooleanField(
        verbose_name=_(
            'Will the CEOs be investing money from their own pockets?'),
        choices=YES_NO,
        blank=False,
        default=False,
    )
    gender = models.CharField(max_length=6,
                              choices=(('male', _('Male')),
                                       ('female', _('Female')),
                                       ('both', _('Both')),
                                       ('other', _('Other')),),
                              verbose_name=_("What are the owner's genders?"),
                              )
    entity_type = models.CharField(
        max_length=255,
        choices=ENTITY_TYPES_SEARCH,
        verbose_name=_('What is the business structure?'))
    industry = models.CharField(
        max_length=255,
        choices=INDUSTRIES_SEARCH,
        verbose_name=_('What industry is your business?'))
    locations = ArrayField(
        models.CharField(max_length=255, choices=LOCATIONS_SEARCH),
        default=list,
        verbose_name=_('Where are the physical locations of your businesses?'),
    )
    employees = models.IntegerField(verbose_name=_(
        'How many full time employees do you have?'))
    years_in_business = models.IntegerField(
        verbose_name=_('How many years have you been in business?'))
    annual_revenue = models.IntegerField(
        verbose_name=_(
            'What was the gross revenue for your last fiscal calendar year?'))

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
