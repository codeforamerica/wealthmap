import os
import csv

from django.core.management.base import BaseCommand, CommandError
from primerpeso import models


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
                employees=r['currentEmployeesRequired'][1:-1].replace('_', ',').split(',')
                if len(employees) == 1:
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
                print('%s %s' % (employees_min, employees_max))
"""
                opportunity = models.Opportunity(
                    id=r['id'],
                    title=r['title'],
                    locations=r['eligibleBusinessLocation'],
                    application_cost=r['applicationCost'],
                    application_deadline=r['applicationDeadline'],
                    average_application_time=r['avgApplicationTime'],
                    benefit_description=r['benefitDescription'],
                    agency_contact_name=r['agencyContactName'],
                    agency_contact_email=r['agencyContactEmail'],
                    agency_contact_phone=r['agencyContactPhone'],
                    minimum_years_in_business=r['minimumYearsInBusiness'],
                    entity_types=r['eligibleEntityTypes'],
                    =r['annualRevenue'],
                    =r['eligibleIndustries'],
                    =r['gender'],
                    =r['additionalDemographics'],
                    =r['additionalGeneralInformation'],
                    =r['investingOwnMoney'],
                    =r['moneyInvested'],
                    =r['purpose'],
                    =r['age'],
                    =r['benefitType'],
                    =r['agencyId'],
                )
                opportunity.save()
"""
