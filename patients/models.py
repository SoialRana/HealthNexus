from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.
User = get_user_model()

GENDER_CHOICES=(
    ('Male','Male'),
    ('Female','Female'),
    ('other','other'),
)
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_no=models.CharField(max_length=11,unique=True)
    address=models.TextField(default='Dhaka,Bangladesh')
    country=models.CharField(max_length=50,default='Bangladesh')
    date_of_birth=models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=15,choices=GENDER_CHOICES,default='Male')
    image=models.ImageField(upload_to='patients/images/')
    
    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name} {self.user.email}"
    