from django.core.management.base import BaseCommand
from airline_reservation_system.models import APICounter

class Command(BaseCommand):
    help = 'Set the value of the API counter'

    def add_arguments(self, parser):
        parser.add_argument('value', type=int, help='The new value for the API counter')

    def handle(self, *args, **options):
        value = options['value']
        counter = APICounter.objects.first()
        if counter:
            counter.count = value
            counter.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set the API counter value to {value}'))
        else:
            self.stdout.write(self.style.ERROR('API counter does not exist'))