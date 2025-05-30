from django.db import models
from django.utils.translation import gettext_lazy as _

class ContentType(models.TextChoices):
    TEXT = 'text', _('Text')
    VIDEO = 'video', _('Video')
    AUDIO = 'audio', _('Audio')
    FILE = 'file', _('File')
    LINK = 'link', _('Link')

class CourseContent(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='contents')
    type = models.CharField(max_length=20, choices=ContentType.choices, default=ContentType.TEXT)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    order = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order']
        indexes = [
            models.Index(fields=['course', 'order']),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title if self.title else 'Untitled'}" 