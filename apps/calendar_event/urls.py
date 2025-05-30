from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarEventViewSet

router = DefaultRouter()
router.register(r'calendar-events', CalendarEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 