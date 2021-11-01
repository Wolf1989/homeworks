import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        # поле slug добавляется с помощью метода save
        # см. class Phone в phones.models
        for phone in phones:
            Phone.objects.create(
                name=phone['name'],
                image=phone['image'],
                price=phone['price'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'],
            )
        return 'Data from "phones.csv" has been imported.'
