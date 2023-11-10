from rest_framework import viewsets

from todo import models, serializers


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = models.ToDo.objects.all().order_by("-created_at")
    serializer_class = serializers.ToDoSerializer
