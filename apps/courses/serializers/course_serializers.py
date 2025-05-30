from rest_framework import serializers
from ..models.course import Course

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'slug',
            'description', 
            'status', 
            'published_at',
            'created_at',
            'updated_at',
            'teacher_name'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'teacher_name'] 