from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .tasks import *
from drf_spectacular.utils import extend_schema
from .tasks import *
from celery.result import AsyncResult
from monitoring.models import *
from monitoring.utils import *

# Create your views here.

# Register
class UserRegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        
        otp_obj = OTP.objects.create(email=user.email)
        
        send_otp.delay(otp_obj.id)
   
   
@extend_schema(
    request=userLoginSerializer,
    responses={200, dict}
)
# Login    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = userLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response({
                'error': 'Invalid email or password.'
            }, status=401)
            
        create_log(
            user=user,
            action='login'
        )
          
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        
        respone = Response({
            'message': 'Login successfully.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.name
            }
        }, status=200)
        
        respone.set_cookie(
            key = 'access_token',
            value = access_token,
            httponly = True,
            secure = False,
            samesite = 'Lax',
            path = '/'
        )
    
        respone.set_cookie(
            key = 'refresh_token',
            value= str(refresh_token),
            httponly= True,
            secure= False,
            samesite= 'Lax',
            path= '/'
        )
        return respone

# Refresh Token
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        try:
            if refresh_token is None:
                return Response({
                    'error': 'Refresh token not found.'
                }, status=401)
                
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            response = Response({
                'message': 'Access token refreshed successfully.'
            }, status=200)
            
            response.set_cookie(
                key = 'access_token',
                value = access_token,
                httponly = True,
                secure = False,
                samesite = 'Lax',
                path = '/'
            )
            return response
        
        except (TokenError):
            return Response({
                'error': 'Invalid refresh token.'
            }, status=401)
        
# Password Change    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        user = request.user
        
        if not user.check_password(request.data.get('old_password')):
            return Response({
                'error': 'Old password is incorrect.'
            }, status=400)
            
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({
            'message': 'Password changed successfully.'
        }, status=200)
   
# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        create_log(
            user=request.user,
            action='Logout'
        )
        
        response = Response({
            'message': 'Logout successfully.'
        }, status=200)
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
     
# Dashboard   
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        return Response({
            'message': f"Welcome to the dashboard {user.username}!",
            'email': f"Your email is {user.email}"
        })
        
class GenerateOTP(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        email = request.data.get('email')
        
        otp_obj = OTP.objects.create(email=email)
        
        task = send_otp.delay(otp_obj.id)
        
        return Response({
            'message': 'OTP generated and Email sent.',
            'otp_id': otp_obj.id,
            'task_id': task.id
        })
        
class VerifyOTP(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        try:
            otp_obj = OTP.objects.filter(email=email, otp=otp).latest('created_at')
            
            otp_obj.is_verified = True
            otp_obj.save()
            
            return Response({
                'message': 'OTP verified successfully'
            })
            
        except OTP.DoesNotExist:
            return Response({
                'message': 'Invalid OTP and Email.'
            }, status=400)
            
class TaskStatusView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, task_id):
        
        result = AsyncResult(task_id)
        
        return Response({
            'task_id': task_id,
            'status': result.status,
            'result': result.result
        })