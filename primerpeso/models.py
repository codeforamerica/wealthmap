from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField, USPostalCodeField


class WhoAndWhenBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class Agency(WhoAndWhenBase):
    name = models.CharField(max_length=255, unique=True)
    mission = models.TextField(blank=True)
    phone = models.CharField(blank=True, max_length=255)
    fax = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    municipality = models.CharField(blank=True, max_length=255)
    state = USStateField(blank=True)
    postal_code = USPostalCodeField(blank=True)  # zip is a global function
    web = models.URLField(max_length=255, blank=True)


class Requirement(WhoAndWhenBase):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    provider = models.CharField(blank=True, max_length=255)
    link = models.TextField(blank=True)
    cost = models.TextField(blank=True)


class Oppurtunity(WhoAndWhenBase):
    title = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=6,
                              choices=(('male', _('Male')),
                                       ('female', _('Female')),
                                       ('any', _('Any')),
                                       ('other', _('Other')),))
    application_cost = models.IntegerField()
    application_deadline = models.DateField()
    benefit_description = models.TextField()
    agency_contact_name = models.CharField(max_length=255)
    agency_contact_phone = models.CharField(max_length=255)
    agency_contact_email = models.EmailField()
    minimum_years_in_business = models.IntegerField()
    additional_information = models.TextField()
    investing_own_money = models.BooleanField()
    money_invested = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency)
    requirement = models.ManyToMany(Requirement)
    age_min = models.IntegerField()
    age_max = models.IntegerField(null=True, blank=True)
    employees_min = models.IntegerField()
    employees_max = models.IntegerField(null=True, blank=True)
    annual_revenue_min = models.IntegerField()
    annual_revenue_max = models.IntegerField(null=True, blank=True)

    _average_application_time = models.CharField(max_length=255, blank=True)
    """
    Convert to Many to Many with a single field for location.
    eligibleBusinessLocation     | character varying(255)[] | not null

    Use this tutorial https://bradmontgomery.net/blog/nice-arrayfield-widgets-choices-and-chosenjs/
    eligibleEntityTypes          | character varying(255)[] | not null
    eligibleIndustries           | character varying(255)[] | not null
    additionalDemographics       | character varying(255)[] |
    benefitType                  | character varying(255)[] | not null default ARRAY['incentive'::character varying]
    purpose                      | text[]                   | not null default ARRAY['anything'::text]

    """

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Oppurtunities'
