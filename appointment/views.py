from django.shortcuts import render
from rest_framework import viewsets
from .models import Apointment 
from .serializers import AppointmentSerializer

# Create your views here.

class AppointmentView(viewsets.ModelViewSet):
    queryset=Apointment.objects.all()
    serializer_class=AppointmentSerializer
    
    # we use get queryset() for custom queryset
    def get_queryset(self):
        queryset= super().get_queryset()
        patient_id=self.request.query_params.get('patient_id')
        if patient_id:
            queryset=queryset.filter(patient_id=patient_id)
        return queryset