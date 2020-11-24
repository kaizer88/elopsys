from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
import datetime
class Command(BaseCommand):
    help = 'Create the base set of Groups and Permissions'

    def handle(self, *args, **options):
        groups = ['Administrator', 
                  'Emerald HR User', 
                  'Emerald Employee', 
                  'Technician', 
                  'Fleet Administrators', 
                  'Management',
                  'Regional Manager']
        for grp in groups:
            Group.objects.get_or_create(name=grp)
        
