from django.shortcuts import render
from .models import Service
from rest_framework import viewsets
from .serializers import ServiceSerializer
# Create your views here.

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class=ServiceSerializer
    