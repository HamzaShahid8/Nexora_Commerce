from rest_framework import serializers
from .models import *
from .services import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        search_fields = ['id', 'name', 'created_by']
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']
        search_fields = ['id', 'name', 'created_by']
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    brand = BrandSerializer(required=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'brand', 'description', 'is_active', 'created_by']
        
class ProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'product', 'image', 'price', 'color', 'size', 'created_by']
        read_only_fields = ['sku']
        
    def create(self, validated_data):
        return create_product_variant(validated_data)
    
    def update(self, instance, validated_data):
        return update_product_variant(instance, validated_data)