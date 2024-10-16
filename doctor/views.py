from django.shortcuts import render
from .models import Doctor,Designation,Specialization,AvailableTime,Review
from .serializers import DesignationSerializer,DoctorSerializer,SpecializationSerializer,AvailableTimeSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
# Create your views here.

class DoctorView(viewsets.ModelViewSet):
    queryset=Doctor.objects.all()
    serializer_class=DoctorSerializer
    
class SpecializationView(viewsets.ModelViewSet):
    queryset=Specialization.objects.all()
    serializer_class=SpecializationSerializer
    
class DesignationView(viewsets.ModelViewSet):
    queryset=Designation.objects.all()
    serializer_class=DesignationSerializer
    
class AvailableTimeView(viewsets.ModelViewSet):
    queryset=AvailableTime.objects.all()
    serializer_class=AvailableTimeSerializer
    
class ReviewView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer