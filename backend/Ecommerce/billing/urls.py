from rest_framework.routers import DefaultRouter
from .models import *
from .views import *
from django.urls import path, include

router = DefaultRouter()

router.register('invoice', InvoiceViewSet, basename='invoice')
router.register('invoice_items', InvoiceItemViewSet, basename='invoice_items')

urlpatterns = [
    path('', include(router.urls)),
]