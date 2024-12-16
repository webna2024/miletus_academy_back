from django.test import TestCase
from lessons.models import LessonModel

class LessonTets(TestCase):

    @classmethod
    def setUpTestData(cls):
        LessonModel.objects.create(title="python3",
                                   description="this is a test lesson for python3",
                                   week_number=3)
        
    def test_title_content(self):
        lesson = LessonModel.objects.get(id=1)
        expected_object_name = f'{lesson.title}'
        self.assertEqual(expected_object_name, 'first lesson')
    
    def Lesson_description(self):
        lesson = LessonModel.objects.get(id=1)
        expected_object_name = f'{lesson.description}'
        self.assertEqual(expected_object_name, 'the description of first lesson')
