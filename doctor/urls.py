from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet,
    DesignationViewSet,
    SpecializationViewSet,
    AvailableTimeViewSet,
    ReviewViewSet
)

router = DefaultRouter()
router.register('list', DoctorViewSet)
router.register('designation', DesignationViewSet)
router.register('specialization', SpecializationViewSet)
router.register('available_time', AvailableTimeViewSet)
router.register('reviews', ReviewViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]