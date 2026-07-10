import stripe
from orders.models import *
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    
    @staticmethod
    def create_checkout_session(payment):
        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            mode = 'payment',
            
            line_items = [
                {
                    'price_data': {
                        'currency': payment.currency,
                        'product_data': {
                            'name': f"Order - {payment.order.code}"
                        },
                        'unit_amount': int(payment.amount * 100)
                    },
                    'quantity': 1,
                }
            ],
            metadata = {
                'payment_id': payment.pk,
                'order_id': payment.order.pk,
            },
            success_url="http://localhost:5173/payment-success",

            cancel_url="http://localhost:5173/payment-cancel",
        )
        
        payment.checkout_session_id = session.id
        payment.save(update_fields=["checkout_session_id"])
        
        return session