from django.core.management.base import BaseCommand
from products.models import *

class Command(BaseCommand):
    help = 'Create Product Variant'
    
    def handle(self, *args, **kwargs):
        
        VARIANTS = [
            ("iPhone 17", 329999, "Black", "256GB"),
            ("iPhone 18", 400000, "Black", "256GB"),
            ('iPhone 17 Pro Max', 400000, "Black", "256GB"),
            ("Galaxy S25 Ultra", 299999, "Silver", "512GB"),
            ("Pixel 10 Pro", 249999, "White", "256GB"),
            ("OnePlus 14", 189999, "Green", "256GB"),
            ("MacBook Pro M4", 549999, "Space Black", "16GB/512GB"),
            ("Dell XPS 15", 429999, "Silver", "16GB/1TB"),
            ("HP Spectre x360", 389999, "Blue", "16GB/512GB"),
            ("Lenovo ThinkPad X1", 409999, "Black", "32GB/1TB"),
            ("ASUS ROG Strix G16", 459999, "Black", "32GB/1TB"),
            ("MSI Stealth 16", 479999, "Gray", "32GB/1TB"),
            ("iPad Pro M4", 289999, "Silver", "256GB"),
            ("Galaxy Tab S10", 219999, "Gray", "256GB"),
            ("Sony WH-1000XM6", 109999, "Black", "Standard"),
            ("JBL Charge 6", 49999, "Blue", "Standard"),
            ("Canon EOS R8", 399999, "Black", "Body Only"),
            ("Nikon Z6 III", 489999, "Black", "Body Only"),
            ("Logitech MX Master 3S", 34999, "Graphite", "Standard"),
            ("Anker Power Bank 20000mAh", 19999, "Black", "20000mAh"),
            ("LG OLED C5", 699999, "Black", '65"'),
            ("PlayStation 5 Pro", 259999, "White", "1TB"),
        ]
        
        for product_name, price, color, size in VARIANTS:
            
            product = Product.objects.get(name=product_name)
            
            ProductVariant.objects.get_or_create(
                product=product,
                color=color,
                size=size,
                sku=f"SKU-{uuid.uuid4().hex[:8].upper()}",
                defaults = {
                    'price': price
                }
            )
            
            self.stdout.write(self.style.SUCCESS('Product Variants created successfully.'))