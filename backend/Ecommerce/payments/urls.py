from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    CheckoutAPIView,
    StripeWebhookAPIView,
)

router = DefaultRouter()

router.register(
    "payments",
    PaymentViewSet,
    basename="payments",
)

urlpatterns = [

    path(
        "",
        include(router.urls),
    ),

    path(
        "checkout/",
        CheckoutAPIView.as_view(),
        name="checkout",
    ),

    path(
        "webhook/",
        StripeWebhookAPIView.as_view(),
        name="webhook",
    ),
]