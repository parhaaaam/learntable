from rest_framework import viewsets, permissions
from apps.courses.models import CourseInstance
from .serializers import CourseInstanceSerializer

class CourseInstanceViewSet(viewsets.ModelViewSet):
    queryset = CourseInstance.objects.all()
    serializer_class = CourseInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id', None)
        teacher_id = self.request.query_params.get('teacher_id', None)
        
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        if teacher_id is not None:
            queryset = queryset.filter(teacher_id=teacher_id)
            
        return queryset 