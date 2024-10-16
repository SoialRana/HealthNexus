from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,email, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        ) 

        user.set_password(password)
        user.save(using=self._db) 
        return user

    def create_superuser(self, email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        # Create a new superuser
        user = self.create_user(
            email,password,**extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(max_length=100, unique=True)
    username        = models.CharField(max_length=50,null=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)

    # Specify the custom user manager
    objects = MyAccountManager() 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def full_name(self): 
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return str(self.id)+"-"+ self.email    
    def get_email(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True