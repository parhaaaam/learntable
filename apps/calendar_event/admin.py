from django.contrib import admin
from .models import CalendarEvent

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'course_instance', 'starts_at', 'ends_at', 'created_at', 'updated_at')
    list_filter = ('user', 'course_instance', 'starts_at', 'ends_at')
    search_fields = ('title', 'user__username', 'course_instance__name')
    ordering = ('-starts_at',) 