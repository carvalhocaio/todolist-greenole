from django.test import TestCase

from todo import models, serializers


class ToDoSerializerTestCase(TestCase):
    def setUp(self):
        self.todo = models.ToDo.objects.create(title="ToDo Test", description="Testing")
        self.serializer = serializers.ToDoSerializer(instance=self.todo)

    def test_verify_fields_serialized(self):
        data = self.serializer.data
        self.assertEquals(
            set(data.keys()),
            {
                "id",
                "status_display",
                "created_at",
                "updated_at",
                "title",
                "description",
            },
        )
