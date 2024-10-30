from django.contrib import admin
from lessons.models import LessonModel

# Register your models here.

class LessonAdminPage(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'order', 'create_at',)
    search_fields = ('title', 'course_id',)
    ordering = ('title',)

admin.site.register(LessonModel, LessonAdminPage)
