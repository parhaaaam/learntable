from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class RequestStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')

class CourseRequest(models.Model):
    course_instance = models.ForeignKey('courses.CourseInstance', on_delete=models.CASCADE, related_name='requests')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_requests')
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['course_instance', 'student']
        indexes = [
            models.Index(fields=['course_instance', 'student', 'status']),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.course_instance.course.title}" 