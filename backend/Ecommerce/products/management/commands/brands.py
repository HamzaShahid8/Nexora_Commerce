from django.core.management.base import BaseCommand
from products.models import *

class Command(BaseCommand):
    help = 'Create brands.'
    
    def handle(self, *args, **kwargs):
        
        brand_names = [
            'Samsung',
            'Apple',
            'Samsung',
            'Xiaomi',
            'OnePlus',
            'Google',
            'Oppo',
            'Apple',
            'Dell',
            'HP',
            'Lenovo',
            'Microsoft',
            'Dell',
            'HP',
            'Lenovo',
            'Apple',
            'Samsung',
            'Lenovo',
            'Huawei',
            'Xiaomi',
            'Microsoft',
            'JBL',
            'Canon',
            'Nikon',
            'Microsoft',
            "ASUS",
            "MSI",
            "Sony",
            "Logitech",
            "Anker",
            "LG",
        ]
        
        for name in brand_names:
            brand, created = Brand.objects.get_or_create(name=name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Brands {name} created successfully."))
                
            else:
                self.stdout.write(self.style.WARNING(f"Brands {name} already exists."))
                
        self.stdout.write(self.style.SUCCESS(f"Brands {name} seeding successfully."))