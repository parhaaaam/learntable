from django.db import models
from django.conf import settings
from apps.courses.models.course_instance import CourseInstance

class CalendarEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_events'
    )
    course_instance = models.ForeignKey(
        CourseInstance,
        on_delete=models.CASCADE,
        related_name='calendar_events'
    )
    title = models.CharField(max_length=255)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'calendar_events'
        ordering = ['-starts_at']

    def __str__(self):
        return f"{self.title} ({self.starts_at} - {self.ends_at})" 