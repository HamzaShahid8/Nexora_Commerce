from django.core.management.base import BaseCommand
from products.models import *

class Command(BaseCommand):
    help = 'Create Categories'
    
    def handle(self, *args, **kwargs):
        categories = [
            'Electronics',
            'Mobiles',
            'Laptops',
            'Computers',
            'Tablets',
            'Accessories',
            'Audio',
            'Cameras',
           'Gaming',
        ]
        
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Categories {category_name} created."))
                
            else:
                self.stdout.write(self.style.WARNING(f"Categories {category_name} already exists."))
                
        self.stdout.write(self.style.SUCCESS(f"Categories seeding successfully."))