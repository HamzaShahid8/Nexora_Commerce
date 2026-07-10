from django.core.management.base import BaseCommand
from roles_permissions.models import *

class Command(BaseCommand):
    help = 'Create permissions'
    
    def handle(self, *args, **kwargs):
        permission_names = [
            'create_profile',
            'update_profile',
            'delete_profile',
            'view_profile',
            'create_role',
            'update_role',
            'delete_role',
            'view_role',
            'create_permission',
            'update_permission',
            'view_permission',
            'delete_permission',
            'create_role_permission',
            'update_role_permission',
            'delete_role_permission',
            'view_role_permission',
            'create_category',
            'update_category',
            'delete_category',
            'view_category',
            'create_brand',
            'update_brand',
            'delete_brand',
            'view_brand',
            'create_product',
            'update_product',
            'delete_product',
            'view_product',
            'create_product_variant',
            'update_product_variant',
            'delete_product_variant',
            'view_product_variant',
            'create_order',
            'update_order',
            'delete_order',
            'view_order',
            'create_orderitem',
            'update_orderitem',
            'delete_orderitem',
            'view_orderitem',
            'view_payment',
            'checkout_payment',
            'refund_payment',
            'create_bill',
            'update_bill',
            'delete_bill',
            'view_bill',
            'create_bill_item',
            'update_bill_item',
            'delete_bill_item',
            'view_bill_item',
        ]
        
        for name in permission_names:
            permission, created = Permissions.objects.get_or_create(name=name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Permissions created: {name}"))
                
            else:
                self.stdout.write(self.style.WARNING(f"Permissions already exists: {name}"))
                
        self.stdout.write(self.style.SUCCESS(f"Permissions seeding completed"))