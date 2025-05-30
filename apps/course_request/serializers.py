from rest_framework import serializers
from apps.courses.models import CourseRequest
 
class CourseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = ['id', 'course_instance', 'student', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 