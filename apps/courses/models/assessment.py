from django.db import models
from django.utils.translation import gettext_lazy as _

class AssessmentType(models.TextChoices):
    ASSIGNMENT = 'assignment', _('Assignment')
    QUIZ = 'quiz', _('Quiz')
    EXAM = 'exam', _('Exam')
    PROJECT = 'project', _('Project')

class Assessment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=AssessmentType.choices, default=AssessmentType.ASSIGNMENT)
    instructions = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['course', 'due_date']),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}" 