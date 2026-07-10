from .models import *

def create_log(user, action, manager_profile=None, worker_profile=None, customer_profile=None, product=None, product_variant=None, order=None, order_item=None, payment=None, invoice=None, invoice_item=None):
    
    if not user or not user.is_authenticated:
        return None
    
    return ActivityLogs.objects.create(
        user=user,
        action=action,
        manager_profile=manager_profile,
        worker_profile=worker_profile,
        customer_profile=customer_profile,
        product=product,
        product_variant=product_variant,
        order=order,
        order_item=order_item,
        payment=payment,
        invoice=invoice,
        invoice_item=invoice_item
    )