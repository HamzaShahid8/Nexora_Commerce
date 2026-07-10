from rest_framework.routers import DefaultRouter
from .views import *
from .models import *
from .serializers import *
from django.urls import path, include

router = DefaultRouter()

router.register('roles', RolesViewSet, basename='roles')
router.register('permissions', PermissionsViewSet, basename='permissions')
router.register('roles_permissions', RolesPermissionsViewSet, basename="roles_permissions")

urlpatterns = [
    path('', include(router.urls)),
]