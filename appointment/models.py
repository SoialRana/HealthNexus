from django.db import models
from patients.models import Patient
from doctor.models import Doctor,AvailableTime
# Create your models here.

APOINTMENT_TYPES=[
    ('Online','Online'),
    ('Offline','Offline'),
]
APOINTMENT_STATUS=[
    ('Pending','Pending'),
    ('Running','Running'),
    ('Complete','Complete'),
]
class Apointment(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    apointment_types=models.CharField(max_length=10,choices=APOINTMENT_TYPES)
    apointment_status=models.CharField(max_length=10,choices=APOINTMENT_STATUS,default="Pending")
    time=models.ForeignKey(AvailableTime,on_delete=models.CASCADE)
    symptom=models.TextField()
    cancel=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient- {self.patient.user.first_name} Doctor-{self.doctor.user.first_name}"