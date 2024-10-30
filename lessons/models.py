from django.db import models
from courses.models import course
# Create your models here.

class LessonModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.OneToOneField(course, on_delete=models.CASCADE, related_name="lessons")
    week_number = models.IntegerField()
    order = models.IntegerField()
    content_type = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
     
