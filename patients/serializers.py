from rest_framework import serializers
from .models import Patient
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
class PatientSerializer(serializers.ModelSerializer):
    # user=serializers.StringRelatedField(many=False) # as we use one to one relation user with patient so Many=False, if we will use ForeignKey then we use many=True
    class Meta:
        model=Patient
        fields='__all__'
        
        
''' class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','confirm_password']
        
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        password=self.validated_data['password']
        password2=self.validated_data['confirm_password']
        
        if password!=password2:
            raise serializers.ValidationError({'errors': 'Password does not match'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'errors': 'user with this email already exists'})
        
        user=User(username=username,email=email)
        user.set_password(password)
        user.save()
        return user '''