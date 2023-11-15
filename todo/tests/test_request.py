from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo import models


class ToDoTestCase(APITestCase):
    def setUp(self):
        self.list_url = reverse("todo-list")

    def test_request_get_to_list_todos(self):
        request = self.client.get(self.list_url)
        self.assertEquals(request.status_code, status.HTTP_200_OK)

    def test_request_get_to_todo_by_id(self):
        data = {"title": "ToDo Test", "description": "Testing get one request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        request = self.client.get(f"{self.list_url}/{todo_id}")
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(
            models.ToDo.objects.get().description, "Testing get one request"
        )

    def test_request_get_to_not_found_todo(self):
        request = self.client.get(f"{self.list_url}/1")
        self.assertEquals(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_post_to_create_todo(self):
        data = {"title": "ToDo Test", "description": "testing request"}
        request = self.client.post(self.list_url, data=data)
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(models.ToDo.objects.count(), 1)
        self.assertEquals(models.ToDo.objects.get().title, "ToDo Test")

    def test_request_post_to_create_multiples_todos(self):
        data = [
            {"title": "ToDo Test 001", "description": "testing request A"},
            {"title": "ToDo Test 002", "description": "testing request B"},
            {"title": "ToDo Test 003", "description": "testing request C"},
        ]
        request = self.client.post(self.list_url, data=data)
        self.assertEquals(request.status_code, status.HTTP_201_CREATED)
        self.assertEquals(models.ToDo.objects.count(), 3)

    def test_request_post_to_create_todo_with_invalid_status(self):
        data = {"title": "ToDo Test", "status": "invalid status"}
        request = self.client.post(self.list_url, data=data)
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_delete_to_delete_todo(self):
        data = {"title": "Test ToDo", "description": "Testing delete request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        request = self.client.delete(f"{self.list_url}/{todo_id}")
        self.assertEquals(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_delete_to_not_found_todo(self):
        request = self.client.delete(f"{self.list_url}/1")
        self.assertEquals(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_patch_to_update_todo(self):
        data = {"title": "Test ToDo", "description": "Testing patch request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        data_update = {"status": "CONCLUDED"}
        request = self.client.patch(f"{self.list_url}/{todo_id}", data=data_update)
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(models.ToDo.objects.get().status, "CONCLUDED")

    def test_request_patch_to_update_todo_with_invalid_status(self):
        data = {"title": "Test ToDo", "description": "Testing patch request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        data_update = {"status": "status"}
        request = self.client.patch(f"{self.list_url}/{todo_id}", data=data_update)
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_put_to_update_todo(self):
        data = {"title": "Test ToDo", "description": "Testing put request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        data_update = {"title": "title", "status": "CONCLUDED"}
        request = self.client.put(f"{self.list_url}/{todo_id}", data=data_update)
        self.assertEquals(request.status_code, status.HTTP_200_OK)
        self.assertEquals(models.ToDo.objects.get().status, "CONCLUDED")

    def test_request_put_to_update_todo_with_invalid_status(self):
        data = {"title": "Test ToDo", "description": "Testing put request"}
        request_create = self.client.post(self.list_url, data=data)

        todo_id = request_create.data["id"]
        data_update = {"title": "title", "status": "status"}
        request = self.client.put(f"{self.list_url}/{todo_id}", data=data_update)
        self.assertEquals(request.status_code, status.HTTP_400_BAD_REQUEST)
