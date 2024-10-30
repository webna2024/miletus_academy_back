from rest_framework import viewsets
from .models import LessonModel
from .serializers import LessonSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
