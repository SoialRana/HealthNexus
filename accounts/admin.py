from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username','email', 'first_name', 'last_name','is_active') 
admin.site.register(User, AccountAdmin)