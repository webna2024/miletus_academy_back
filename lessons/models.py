from django.db import models

# Create your models here.

class LessonModel(models.Model):
    title = models.CharField(
        max_length=255,
    )
    content = models.TextField()
    course_id = models.OneToOneField()
    week_number = models.IntegerField()
    order = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=500)

    def __str__(self):
        return self.title
     
