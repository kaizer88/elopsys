from django.core.management.base import BaseCommand, CommandError
from employees.models import Employee

class Command(BaseCommand):
    help = 'Creates sample employees for testing'

    def handle(self, *args, **options):
        
        x = 0
        # while x < 5:
        #     Employee.objects.get_or_create(first_name="Sam_{}".format(x),
        #                                    last_name="Pill_{}".format(x),
        #                                    id_number="908398388480_{}".format(x),
        #                                    division='marketing', role='AG',
        #                                    imported=False)
        #     x += 1
