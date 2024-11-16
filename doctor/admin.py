from django.contrib import admin
from .models import AvailableTime,Designation,Specialization,Doctor,Review,MedicalRecord
# Register your models here.

admin.site.register(AvailableTime)

class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',),}
admin.site.register(Designation,DesignationAdmin)

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',),}
admin.site.register(Specialization,SpecializationAdmin)

admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(MedicalRecord)