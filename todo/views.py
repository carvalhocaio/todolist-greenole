from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


from todo import models, serializers


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = models.ToDo.objects.all().order_by("-created_at")
    serializer_class = serializers.ToDoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["title", "description"]
