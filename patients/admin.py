from django.contrib import admin
from .models import Patient
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display=['get_first_name','get_last_name','mobile_no','image']
    
    def get_first_name(self,obj):
        return obj.user.first_name
    
    def get_last_name(self,obj):
        return obj.user.last_name
    get_first_name.short_description = 'First Name'
    get_last_name.short_description = 'Last Name'
admin.site.register(Patient,PatientAdmin)