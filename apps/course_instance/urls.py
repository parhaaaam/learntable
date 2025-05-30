from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseInstanceViewSet

router = DefaultRouter()
router.register(r'course-instances', CourseInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 