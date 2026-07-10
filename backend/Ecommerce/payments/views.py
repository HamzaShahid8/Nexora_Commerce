from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
import stripe
from django.conf import settings
from .models import Payment
from .serializers import (
    PaymentReadSerializer,
    PaymentWriteSerializer,
    CheckoutSerializer,
)
from .services import PaymentService
from roles_permissions.permissions import HasPermission
from monitoring.models import *
from monitoring.utils import *


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Payment.objects.select_related(
        "order",
        "order__user",
    ).all()

    permission_classes = [
        IsAuthenticated,
        HasPermission,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "provider",
        "status",
        "currency",
    ]

    search_fields = [
        "code",
        "payment_intent",
        "checkout_session_id",
        "order__code",
        "order__user__username",
    ]

    ordering_fields = [
        "created_at",
        "amount",
        "paid_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):
        return PaymentReadSerializer
    
    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()
        
        create_log(
            user=self.request.user,
            action='view',
            payment=payment,
            order=payment.order
        )
        return super().retrieve(*request, *args, **kwargs)

    def get_queryset(self):

        user = self.request.user

        if user.role and user.role.name == "manager":
            return self.queryset

        return self.queryset.filter(order__user=user)

    def get_permissions(self):

        permission = HasPermission()
        permission.required_permission = "view_payment"

        return [
            IsAuthenticated(),
            permission,
        ]


class CheckoutAPIView(APIView):       # jb user pay now pr click krta h to yay call hota h

    permission_classes = [
        IsAuthenticated,
        HasPermission,
    ]

    def post(self, request):

        serializer = CheckoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )
        
        # payment get kro us payment ka code get kro, and us code kay order ka user get kro
        payment = get_object_or_404(

            Payment,

            code=serializer.validated_data[
                "payment_code"
            ],

            order__user=request.user,
        )

        session = PaymentService.create_checkout_session(
            payment
        )

        return Response(
            {
                "checkout_url": session.url
            },
            status=status.HTTP_200_OK,
        )


class StripeWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        payload = request.body

        signature = request.headers.get(
            "Stripe-Signature"
        )

        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
            )

        except Exception:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":

            session = event["data"]["object"]

            from django.utils import timezone

            with transaction.atomic():

                payment = Payment.objects.select_for_update().get(
                    id=session["metadata"]["payment_id"]
                )

                # Duplicate webhook se bachne ke liye
                if payment.status == "paid":
                    return Response(status=200)

                payment.status = "paid"
                payment.payment_intent = session["payment_intent"]
                payment.checkout_session_id = session["id"]
                payment.stripe_response = session
                payment.paid_at = timezone.now()

                payment.save()

                order = payment.order

                order.payment_status = "paid"
                order.status = "paid"

                order.save()

        return Response(status=200)