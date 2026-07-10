from django.core.management.base import BaseCommand
from products.models import *

class Command(BaseCommand):
    help = 'Create products.'
    
    def handle(self, *args, **kwargs):
        PRODUCTS = [
            ('iPhone 17', 'Mobiles', 'Apple'),
            ('iPhone 17 Pro Max', 'Mobiles', 'Apple'),
            ('iPhone 18', 'Mobiles', 'Apple'),
            ("Galaxy S25 Ultra", "Mobiles", "Samsung"),
            ("Pixel 10 Pro", "Mobiles", "Google"),
            ("OnePlus 14", "Mobiles", "OnePlus"),
            ("MacBook Pro M4", "Laptops", "Apple"),
            ("Dell XPS 15", "Laptops", "Dell"),
            ("HP Spectre x360", "Laptops", "HP"),
            ("Lenovo ThinkPad X1", "Laptops", "Lenovo"),
            ("ASUS ROG Strix G16", "Gaming", "ASUS"),
            ("MSI Stealth 16", "Gaming", "MSI"),
            ("iPad Pro M4", "Tablets", "Apple"),
            ("Galaxy Tab S10", "Tablets", "Samsung"),
            ("Sony WH-1000XM6", "Audio", "Sony"),
            ("JBL Charge 6", "Audio", "JBL"),
            ("Canon EOS R8", "Cameras", "Canon"),
            ("Nikon Z6 III", "Cameras", "Nikon"),
            ("Logitech MX Master 3S", "Accessories", "Logitech"),
            ("Anker Power Bank 20000mAh", "Accessories", "Anker"),
            ("LG OLED C5", "Electronics", "LG"),
            ("PlayStation 5 Pro", "Gaming", "Sony"),
        ]
        
        for name, category_name, brand_name in PRODUCTS:
            
            category = Category.objects.get(name=category_name)
            brand = Brand.objects.get(name=brand_name)
            
            Product.objects.get_or_create(
                name=name,
                defaults = {
                    'category': category,
                    'brand': brand,
                    'is_active': True,
                }
            )
            
            self.stdout.write(self.style.SUCCESS('Products created successfully.'))