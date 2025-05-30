from rest_framework import serializers
from apps.courses.models import CourseContent
 
class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['id', 'course', 'type', 'title', 'body', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 