from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from roles_permissions.models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'image']
        
    def validate_email(self, email):
        if not email.endswith('@gmail.com'):
            raise serializers.ValidationError('Email must be a Gmail address.')
        return email
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        image = validated_data.pop('image', None)
        
        customer_role = Roles.objects.get(name='customer')
        
        user = User.objects.create_user(
            role = customer_role,
            **validated_data
        )
        
        if image:
            user.image = image
            
        user.set_password(password)
        user.save()

        return user
    
class userLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(
            username = data['email'],
            password = data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        data['user'] = user
        return data
    
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'otp', 'email', 'is_verified', 'created_at', 'expires_at']