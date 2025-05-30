from rest_framework import serializers
from apps.courses.models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'course', 'title', 'type', 'instructions', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 