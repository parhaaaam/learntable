from django.db import models
from django.conf import settings

class CourseInstance(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='instances')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teaching_instances')
    capacity = models.SmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['course', 'teacher']),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.teacher.name}" 