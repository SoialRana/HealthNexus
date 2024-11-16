from django.urls import path,include
from .import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('list',views.DoctorView)
router.register('specialization',views.SpecializationView)
router.register('designation',views.DesignationView)
router.register('available_time',views.AvailableTimeView)
router.register('review',views.ReviewView)
router.register('medical_record',views.MedicalRecordView)

urlpatterns = [
    path('',include(router.urls)),
]
