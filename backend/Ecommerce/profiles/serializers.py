from rest_framework import serializers
from .models import *
from accounts.models import *

class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='username')
    
    class Meta:
        model = ManagerProfile
        fields = ['code', 'user', 'phn_no', 'address']
        
class WorkerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='username')
    
    class Meta:
        model = WorkerProfile
        fields = ['code', 'user', 'phn_no', 'address']
        
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='username')
    
    class Meta:
        model = CustomerProfile
        fields = ['code', 'user', 'phn_no', 'address']