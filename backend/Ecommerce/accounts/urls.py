from django.urls import path
from .views import *
from .serializers import *
from .models import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('change_password/', PasswordChangeView.as_view(), name = 'change_password'),
    path('refresh/', RefreshTokenView.as_view(), name = 'refresh'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('create_otp/', GenerateOTP.as_view(), name = 'generate_otp'),
    path('verify_otp/', VerifyOTP.as_view(), name = 'verify_otp'),
    path('task_status/', TaskStatusView.as_view(), name = 'task_status'),
]