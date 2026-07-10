from django.shortcuts import render
from .models import *
from  .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ActivityLogsViewSet(viewsets.ModelViewSet):
    queryset = ActivityLogs.objects.all()
    serializer_class = ActivityLogsSerializer
    permission_classes = [IsAuthenticated]