from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.course_views import CourseViewSet
from .views.course_content_views import CourseContentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'course-contents', CourseContentViewSet)

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
] 