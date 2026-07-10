from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationMiddleware:

    def __init__(self, get_response): # app  start hony pr run hoga
        self.get_response = get_response
        
        self.public_paths = [
            '/register/',
            '/login/',
        ]
        
    def __call__(self, request): # ye har request pr run hoga
        if request.path in self.public_paths:
            request.user = AnonymousUser()
            return self.get_response(request)
        
        access_token = request.COOKIES.get('access_token')
        
        if access_token:
            try:
                # check kay token access token e h
                validated_token = AccessToken(access_token)
                
                # token say user id fetch krengy
                user_id = validated_token['user_id']
                
                # database sy user fetch krengy
                user = User.objects.get(id = user_id)
                
                # request.user ko user say set krengy
                request.user = user
                
            except Exception as e:
                # invalid or expired
                request.user = AnonymousUser()
                
        else:
            # token not found
            request.user = AnonymousUser()
            
        response =self.get_response(request)
        return response