from django.urls import path,include
from .views import AppointmentView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('',AppointmentView)

urlpatterns = [
    path('',include(router.urls)),
]
