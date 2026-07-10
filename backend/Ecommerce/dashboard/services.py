from accounts.models import *
from billing.models import *
from orders.models import *
from payments.models import *
from products.models import *
from profiles.models import *
from django.db.models import Sum

class DashboardService:
    
    @staticmethod
    def get_data(user):
        
        if user.role.name == 'manager':
            
            total_categories = Category.objects.count()
            total_brands = Brand.objects.count()
            total_products = Product.objects.count()
            total_variants = ProductVariant.objects.count()
            total_orders = Order.objects.count()
            pending_orders = Order.objects.filter(status='pending').count()
            delivered_orders = Order.objects.filter(status='pending').count()
            paid_orders = Order.objects.filter(status='paid').count()
            total_invoices = Invoice.objects.count()
            total_payments = Payment.objects.count()
            revenue = Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
            recent_orders = list(Order.objects.order_by('-created_at').values()[:10])
            recent_payments = list(Order.objects.order_by('-created_at').values()[:10])
            
            return {
                'total_categories': total_categories,
                'total_brands': total_brands,
                'total_products': total_products,
                'total_variants': total_variants,
                
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'delivered_orders': delivered_orders,
                'paid_orders': paid_orders,
                
                'total_invoices': total_invoices,
                'total_payments': total_payments,
                
                'revenue': revenue,
                'recent_orders': recent_orders,
                'recent_payments': recent_payments,
            }
            
        elif user.role.name == 'customer':
            
            customer_orders = Order.objects.filter(user=user).count()
            orders = list(Order.objects.filter(user=user).values())
            customer_payments = Payment.objects.filter(order__user=user).count()
            payments = list(Payment.objects.filter(order__user=user).values())
            delivered_orders = Order.objects.filter(status='delivered').count()
            delivered = list(Order.objects.filter(status='delivered').values())
            pending_orders = Order.objects.filter(status='pending').count()
            pending = list(Order.objects.filter(status='pending').values())
            cancelled_orders = Order.objects.filter(status='cancelled').count()
            cancelled = list(Order.objects.filter(status='cancelled').values())
            total_spent = Payment.objects.filter(order__user=user).aggregate(total=Sum('amount'))['total'] or 0
            
            return {
                'customer_orders': customer_orders,
                'orders': orders,
                'customer_payments': customer_payments,
                'payments': payments,
                'delivered_orders': delivered_orders,
                'delivered': delivered,
                'pending_orders': pending_orders,
                'pending': pending,
                'cancelled_orders': cancelled_orders,
                'cancelled': cancelled,
                'total_spent': total_spent,
            }
            
        else:
            return {
                'Message': 'Unknown Role'
            }