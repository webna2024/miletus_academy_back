**Accounts App**

models.py:
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField("Courses.Course", related_name="enrolled_students")

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField("Courses.Course", related_name="instructors")
```

serializers.py:
```python
from rest_framework import serializers
from .models import User, Student, Instructor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ["user", "enrolled_courses"]

class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Instructor
        fields = ["user", "courses"]
```

**Courses App**

models.py:
```python
from django.db import models

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

serializers.py:
```python
from rest_framework import serializers
from .models import CourseCategory, Course

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["name", "description", "created_at", "updated_at"]

class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer()

    class Meta:
        model = Course
        fields = ["name", "description", "price", "category", "created_at", "updated_at"]
```

**Lessons App**

models.py:
```python
from django.db import models
from Courses.models import Course

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

serializers.py:
```python
from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["name", "description", "course", "order", "created_at", "updated_at"]
```

**Enrollments App**

models.py:
```python
from django.db import models
from Accounts.models import Student
from Courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress = models.IntegerField(default=0)
```

serializers.py:
```python
from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["student", "course", "started_at", "completed_at", "progress"]
```

**Comments App**

models.py:
```python
from django.db import models
from Accounts.models import User
from Courses.models import Course

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
```

serializers.py:
```python
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "user", "course", "created_at"]
```

This covers the models and serializers for each app in the Miletus online learning platform. Let me know if you have any other questions!

