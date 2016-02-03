import os
import csv

from django.core.management.base import BaseCommand, CommandError
from primerpeso import models


class Command(BaseCommand):
    help = 'Loads in legacy data.'

    def handle(self, *args, **options):
        wd = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(wd,'../../../legacy_data/agency.csv')) as f:
            reader = csv.DictReader(f)
            for agency in reader:
                models.Agency(
                    id=agency['id'],
                    name=agency['name'],
                    mission=agency['mission'],
                    phone=agency['phone'],
                    fax=,email,address,municipality,state,zip,web,creatorId,createdAt,updatedAt 
