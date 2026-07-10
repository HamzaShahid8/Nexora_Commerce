from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()
class Command(BaseCommand):
    help = 'Create a superuser with email and password'
    
    def handle(self, *args, **kwargs):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        
        if not username or not password or not email:
            self.stdout.write(self.style.ERROR('Superuser credentials missing'))
            
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser with this email already exists'))