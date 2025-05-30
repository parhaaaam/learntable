from rest_framework import viewsets, permissions
from apps.courses.models import Assessment
from .serializers import AssessmentSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id', None)
        assessment_type = self.request.query_params.get('type', None)
        
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        if assessment_type is not None:
            queryset = queryset.filter(type=assessment_type)
            
        return queryset.order_by('due_date') 