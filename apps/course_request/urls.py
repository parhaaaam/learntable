from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseRequestViewSet

router = DefaultRouter()
router.register(r'course-requests', CourseRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 