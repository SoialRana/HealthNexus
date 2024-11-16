from django.shortcuts import render
from .models import Doctor,Designation,Specialization,AvailableTime,Review,MedicalRecord
from .serializers import DesignationSerializer,DoctorSerializer,SpecializationSerializer,AvailableTimeSerializer,ReviewSerializer,MedicalRecordSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,BaseFilterBackend
# Create your views here.

class DoctorPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10


class DoctorView(viewsets.ModelViewSet):
    queryset=Doctor.objects.all()
    serializer_class=DoctorSerializer
    pagination_class=DoctorPagination
    filter_backends=[SearchFilter]
    
class SpecializationView(viewsets.ModelViewSet):
    queryset=Specialization.objects.all()
    serializer_class=SpecializationSerializer
    
class DesignationView(viewsets.ModelViewSet):
    queryset=Designation.objects.all()
    serializer_class=DesignationSerializer
    
class AvailableTimeForSpecificDoctor(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor_id=request.query_params.get('doctor_id')
        if doctor_id:
            return queryset.filter(doctor=doctor_id)
        return queryset
            

class AvailableTimeView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=AvailableTime.objects.all()
    serializer_class=AvailableTimeSerializer
    filter_backends=[AvailableTimeForSpecificDoctor]
    
class ReviewView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    
    
class MedicalRecordView(viewsets.ModelViewSet):
    queryset=MedicalRecord.objects.all()
    serializer_class=MedicalRecordSerializer
    
    