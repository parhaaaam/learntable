from rest_framework import serializers
from apps.courses.models import CourseInstance

class CourseInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstance
        fields = ['id', 'course', 'teacher', 'capacity', 'price', 'platform', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 