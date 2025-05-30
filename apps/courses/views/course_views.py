from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.utils import timezone
from ..models.course import Course
from ..serializers.course_serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        """
        This view should return a list of all courses
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Set the user and handle the published_at field when creating a course.
        """
        if serializer.validated_data.get('status') == 'published':
            serializer.save(
                user=self.request.user,
                published_at=timezone.now()
            )
        else:
            serializer.save(user=self.request.user) 