from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from todo import models, serializers


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ToDoSerializer
    queryset = models.ToDo.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status"]
    search_fields = ["title", "description"]
    ordering_fields = "__all__"
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get("limit", None)
        offset = request.query_params.get("offset", None)
        status_filter = request.query_params.get("status", None)
        ordering = request.query_params.get("ordering", None)

        cache_key = f"todo_list_{limit}_{offset}_{status_filter}_{ordering}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())

        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)

        data = {
            "count": queryset.count(),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data,
        }

        cache.set(cache_key, data, timeout=60)

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'todo_{kwargs["pk"]}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        cache.set(cache_key, data, timeout=60)

        return Response(data)
