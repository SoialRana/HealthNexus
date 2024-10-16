from django.shortcuts import render
from .serializers import PatientSerializer
from .models import Patient
from rest_framework import viewsets
# Create your views here.

class PatientView(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class=PatientSerializer
    