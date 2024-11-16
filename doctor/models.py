from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Designation(models.Model):
    name=models.CharField(max_length=40)
    slug=models.SlugField(max_length=50)
    def __str__(self):
        return self.name
    
class Specialization(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField(null=True , blank= True)
    slug=models.SlugField(max_length=50)
    def __str__(self):
        return self.name
    
class AvailableTime(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
# one to many ->> many part e kintu foreignkey add kortam  
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='doctor/images/')
    contact_number=models.CharField(max_length=15,null=True)
    designation=models.ManyToManyField(Designation)
    specialization=models.ManyToManyField(Specialization)
    available_time=models.ManyToManyField(AvailableTime)
    fee=models.IntegerField()
    experience_years=models.PositiveIntegerField(null=True)
    meet_link=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
STAR_CHOICES=[
    ('☆','☆'),
    ('☆☆','☆☆'),
    ('☆☆☆','☆☆☆'),
    ('☆☆☆☆','☆☆☆☆'),
    ('☆☆☆☆☆','☆☆☆☆☆'),
]    
class Review(models.Model):
    reviewer=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    body=models.TextField()
    rating=models.CharField(max_length=10,choices=STAR_CHOICES)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Patient- {self.reviewer.user.first_name} : Doctor- {self.doctor.user.first_name}"
    
    
class MedicalRecord(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=255)
    treatment=models.TextField()
    date=models.DateField()
    
    def __str__(self):
        return f"Patient name : {self.patient.user.first_name}"