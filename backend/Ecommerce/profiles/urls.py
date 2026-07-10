from django.urls import path, include
from .models import *
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('manager_profile', ManagerViewSet, basename='manager_profile')
router.register('worker_profile', WorkerViewSet, basename='worker_profile')
router.register('customer_profile', CustomerViewSet, basename='customer_profile')

urlpatterns = [
    path('', include(router.urls)),
]