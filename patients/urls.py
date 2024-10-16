from django.urls import path,include
from .views import PatientView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('list',PatientView)

urlpatterns = [
    path('',include(router.urls)),
]
