import os
import csv

from django.core.management.base import BaseCommand, CommandError
from primerpeso import models

def get_min_max(data_str):
    employees=data_str[1:-1].replace('_', ',').split(',')
    if 'any' in employees or 'none' in employees:
        employees = employees[0]
        employees_min = 0
        if employees == 'any':
            employees_max = None
        elif employees == 'none':
            employees_max = 0
        else:
            raise Exception('%s is unhandled' % employees)
    else:
        employees_min = employees[0]
        employees_max = employees[-1]
    return (employees_min, employees_max)

def to_array(data_str):
    array = data_str[1:-1].split(',')
    return array

def age_to_range(data_str):
    """
    Currently stored usig a multiple select of these options.
    age: {
      '0': 'Cualquier',
      '1': '16-26',
      '2': '27-35',
      '3': '36-44',
      '4': '45-54',
      '5': '55-64',
      '6': '65+',
    },
    """
    ages=data_str[1:-1].split(',')
    if len(ages)==1 and ages[0]=='0':
        min_age = 16
        max_age = None
    else:
        min_age_str = min(ages)
        max_age_str = max(ages)
        min_dict = { '1': 16, '2': 27, '3': 36, '4': 45, '5': 55, '6': 65 }
        max_dict = { '1': 26, '2': 35, '3': 44, '4': 54, '5': 64, '6': None }
        min_age = min_dict[min_age_str]
        max_age = max_dict[max_age_str]
    return (min_age, max_age)


class Command(BaseCommand):
    help = 'Loads in legacy data.'

    def handle(self, *args, **options):
        wd = os.path.dirname(os.path.realpath(__file__))

        models.Agency.objects.all().delete()
        with open(os.path.join(wd, '../../../legacy_data/agency.csv')) as f:
            reader = csv.DictReader(f)
            for agency in reader:
                agency_instance = models.Agency(
                    id=agency['id'],
                    creator_id=1,
                    name=agency['name'],
                    mission=agency['mission'],
                    phone=agency['phone'],
                    fax=agency['fax'],
                    email=agency['email'],
                    address=agency['address'],
                    municipality=agency['municipality'],
                    state=agency['state'],
                    web=agency['web'],
                    postal_code=agency['zip'],
                )
                agency_instance.save()

        models.Requirement.objects.all().delete()
        with open(os.path.join(wd, '../../../legacy_data/requirement.csv')) as f:
            reader = csv.DictReader(f)
            for r in reader:
                requirement = models.Requirement(
                    id=r['id'],
                    creator_id=1,
                    name=r['name'],
                    description=r['description'],
                    provider=r['reqProvider'],
                    link=r['link'],
                    cost=r['cost'],
                )
                requirement.save()

        models.Opportunity.objects.all().delete()
        with open(os.path.join(wd, '../../../legacy_data/opportunity.csv')) as f:
            reader = csv.DictReader(f)
            for r in reader:
                (employees_min, employees_max) = get_min_max(r['currentEmployeesRequired'])
                (revenue_min, revenue_max) = get_min_max(r['annualRevenue'])
                (age_min, age_max) = age_to_range(r['age'])
                application_deadline=r['applicationDeadline']
                if 'BC' in application_deadline:
                    application_deadline=None
                opportunity = models.Opportunity(
                    id=r['id'],
                    creator_id=1,
                    title=r['title'],
                    locations=to_array(r['eligibleBusinessLocation']),
                    application_cost=r['applicationCost'],
                    application_deadline=application_deadline,
                    average_application_time=r['avgApplicationTime'],
                    benefit_description=r['benefitDescription'],
                    agency_contact_name=r['agencyContactName'],
                    agency_contact_email=r['agencyContactEmail'],
                    agency_contact_phone=r['agencyContactPhone'],
                    minimum_years_in_business=r['minimumYearsInBusiness'],
                    entity_types=to_array(r['eligibleEntityTypes']),
                    industries=to_array(r['eligibleIndustries']),
                    gender=r['gender'],
                    demographics=to_array(r['additionalDemographics']),
                    additional_information=r['additionalGeneralInformation'],
                    investing_own_money=r['investingOwnMoney'],
                    money_invested=r['moneyInvested'],
                    purpose=to_array(r['purpose']),
                    age_min=age_min,
                    age_max=age_max,
                    employees_min=employees_min,
                    employees_max=employees_max,
                    annual_revenue_min=revenue_min,
                    annual_revenue_max=revenue_max,
                    benefit_types=to_array(r['benefitType']),
                    agency_id=r['agencyId'],
                )
                opportunity.save()

        models.RequirementRelationship.objects.all().delete()
        with open(os.path.join(wd, '../../../legacy_data/opp_to_req.csv')) as f:
            reader = csv.DictReader(f)
            for r in reader:
                rr =  models.RequirementRelationship(
                    creator_id='1',
                    opportunity_id=r['opportunityId'],
                    requirement_id=r['requirementId'],
                )
                rr.save()
