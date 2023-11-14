from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from todo import models, serializers


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = models.ToDo.objects.all()
    serializer_class = serializers.ToDoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status"]
    search_fields = ["title", "description"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]
