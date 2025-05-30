from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.courses.models import CourseRequest, RequestStatus
from .serializers import CourseRequestSerializer

class CourseRequestViewSet(viewsets.ModelViewSet):
    queryset = CourseRequest.objects.all()
    serializer_class = CourseRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_instance_id = self.request.query_params.get('course_instance_id', None)
        student_id = self.request.query_params.get('student_id', None)
        status = self.request.query_params.get('status', None)
        
        if course_instance_id is not None:
            queryset = queryset.filter(course_instance_id=course_instance_id)
        if student_id is not None:
            queryset = queryset.filter(student_id=student_id)
        if status is not None:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        course_request = self.get_object()
        course_request.status = RequestStatus.APPROVED
        course_request.save()
        return Response({'status': 'request approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        course_request = self.get_object()
        course_request.status = RequestStatus.REJECTED
        course_request.save()
        return Response({'status': 'request rejected'}) 