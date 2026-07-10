from django.urls import path, include
from .models import *
from .views import *
from .serializers import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('brands', BrandViewSet, basename='brands')
router.register('products', ProductViewSet, basename='products')
router.register('product_variant', ProductVariantViewSet, basename='product_variant')

urlpatterns = [
    path('', include(router.urls)),
]