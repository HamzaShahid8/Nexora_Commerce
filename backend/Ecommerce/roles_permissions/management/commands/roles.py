from django.core.management.base import BaseCommand
from roles_permissions.models import *

class Command(BaseCommand):
    help = 'Create roles'
    
    def handle(self, *args, **kwargs):
        roles = ['manager', 'worker', 'customer']
        
        for role_name in roles:
            role, created = Roles.objects.get_or_create(name=role_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Roles created: {role_name}"))
                
            else:
                self.stdout.write(self.style.WARNING(f"Roles already exists: {role_name}"))
                
        self.stdout.write(self.style.ERROR(f"Roles seeding completed"))