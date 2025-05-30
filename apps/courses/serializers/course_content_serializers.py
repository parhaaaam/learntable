from rest_framework import serializers
from ..models.course_content import CourseContent

class CourseContentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CourseContent
        fields = [
            'id',
            'course',
            'course_title',
            'type',
            'title',
            'body',
            'order',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_order(self, value):
        """
        Check that the order is valid for the course.
        """
        if value < 1:
            raise serializers.ValidationError("Order must be greater than 0")
        return value

    def validate(self, data):
        """
        Check that the order is unique within the course.
        """
        course = data.get('course')
        order = data.get('order')
        instance = self.instance

        # If we're updating and not changing the order, skip validation
        if instance and order == instance.order and course == instance.course:
            return data

        if CourseContent.objects.filter(
            course=course,
            order=order
        ).exclude(id=getattr(instance, 'id', None)).exists():
            raise serializers.ValidationError({
                "order": "Content with this order already exists in this course"
            })
        return data 