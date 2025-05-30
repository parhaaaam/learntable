from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from ..models.course_content import CourseContent
from ..serializers.course_content_serializers import CourseContentSerializer

class CourseContentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows course content to be viewed or edited.
    """
    queryset = CourseContent.objects.all()
    serializer_class = CourseContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter contents by course if course_id is provided.
        """
        queryset = CourseContent.objects.all()
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        return queryset.select_related('course')

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def reorder(self, request):
        """
        Reorder content items within a course.
        Expects data in format:
        {
            "course_id": 1,
            "orders": [
                {"id": 1, "order": 1},
                {"id": 2, "order": 2},
                ...
            ]
        }
        """
        course_id = request.data.get('course_id')
        orders = request.data.get('orders', [])

        if not course_id or not orders:
            return Response(
                {"error": "Both course_id and orders are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify all contents belong to the same course
        content_ids = [item['id'] for item in orders]
        contents = CourseContent.objects.filter(
            id__in=content_ids,
            course_id=course_id
        )

        if len(contents) != len(content_ids):
            return Response(
                {"error": "Invalid content IDs or course ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update orders
        for order_item in orders:
            CourseContent.objects.filter(
                id=order_item['id']
            ).update(order=order_item['order'])

        updated_contents = CourseContent.objects.filter(
            course_id=course_id
        ).order_by('order')
        
        serializer = self.get_serializer(updated_contents, many=True)
        return Response(serializer.data) 