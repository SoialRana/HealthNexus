from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.
User = get_user_model()
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_no=models.CharField(max_length=11)
    image=models.ImageField(upload_to='patients/images/')
    
    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name}"
    