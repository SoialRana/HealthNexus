from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContactUsView

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register('', ContactUsView)

urlpatterns = [
    path('', include(router.urls)),
]