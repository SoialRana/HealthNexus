from django.urls import path,include
from .views import ServiceView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('',ServiceView)

urlpatterns = [
    path('',include(router.urls)),
]
