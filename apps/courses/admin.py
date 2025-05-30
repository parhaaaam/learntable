from django.contrib import admin
from .models import CourseContent, CourseInstance, CourseRequest, Assessment

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'type', 'order', 'created_at')
    list_filter = ('type', 'course')
    search_fields = ('title', 'body')
    ordering = ('course', 'order')

@admin.register(CourseInstance)
class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'capacity', 'price', 'platform', 'created_at')
    list_filter = ('course', 'teacher')
    search_fields = ('course__title', 'teacher__name', 'platform')
    ordering = ('course', 'teacher')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'type', 'due_date', 'created_at')
    list_filter = ('type', 'course', 'due_date')
    search_fields = ('title', 'instructions')
    ordering = ('course', 'due_date')

@admin.register(CourseRequest)
class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_instance', 'status', 'created_at')
    list_filter = ('status', 'course_instance', 'student')
    search_fields = ('student__name', 'course_instance__course__title', 'message')
    ordering = ('-created_at',) 