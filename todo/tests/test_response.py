from django.urls import reverse
from rest_framework.test import APITestCase
from todo import models
from django.core.cache import cache


class ToDoTestCase(APITestCase):
    def setUp(self):
        cache.clear()

        self.list_url = reverse("todo-list")
        self.todos_data = [
            {"title": "ToDo Test 001", "description": "testing response A"},
            {
                "title": "ToDo Test 002",
                "description": "testing response B searching",
                "status": "CONCLUDED",
            },
            {
                "title": "ToDo Test 003 searching",
                "description": "testing response C",
                "status": "CONCLUDED",
            },
        ]
        
        for todo in self.todos_data:
            models.ToDo.objects.create(**todo)

    def test_list_todos(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], len(self.todos_data))

    def test_filter_todos_by_status(self):
        response = self.client.get(f"{self.list_url}?status=CONCLUDED")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        for todo in response.data["results"]:
            self.assertEqual(todo["status_display"], "concluded")

    def test_filter_todos_by_search(self):
        response = self.client.get(f"{self.list_url}?search=searching")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        for todo in response.data["results"]:
            self.assertIn("searching", todo["title"] + todo["description"])

    def test_retrieve_todo_by_id(self):
        todo = self.client.post(self.list_url, {"title": "ToDo Test 004"}).data
        response = self.client.get(f"{self.list_url}/{todo['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], todo["id"])

    def test_create_todo(self):
        data = {"title": "ToDo Test 005", "description": "New ToDo"}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])

    def test_create_todo_with_invalid_status(self):
        data = {"title": "ToDo Test", "status": "INVALID"}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_update_todo_status(self):
        todo = self.client.post(self.list_url, {"title": "ToDo Test 006"}).data
        response = self.client.patch(f"{self.list_url}/{todo['id']}", {"status": "CONCLUDED"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status_display"], "concluded")

    def test_delete_todo(self):
        todo = self.client.post(self.list_url, {"title": "ToDo Test 007"}).data
        response = self.client.delete(f"{self.list_url}/{todo['id']}")
        self.assertEqual(response.status_code, 204)
        get_response = self.client.get(f"{self.list_url}/{todo['id']}")
        self.assertEqual(get_response.status_code, 404)

    def test_response_get_to_list_with_status_concluded(self):
        response = self.client.get(f"{self.list_url}?status=CONCLUDED")

        expected_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": response.data["results"][0]["id"],
                    "status_display": "concluded",
                    "title": "ToDo Test 003 searching",
                    "description": "testing response C",
                },
                {
                    "id": response.data["results"][1]["id"],
                    "status_display": "concluded",
                    "title": "ToDo Test 002",
                    "description": "testing response B searching",
                },
            ],
        }

        actual_results = response.data["results"]
        for result in actual_results:
            result.pop("created_at", None)
            result.pop("updated_at", None)

        expected_results = expected_response["results"]

        self.assertEqual(actual_results, expected_results)
        self.assertEqual(response.data, expected_response)

    def test_response_get_to_list_with_status_in_progress(self):
        response = self.client.get(f"{self.list_url}?status=IN_PROGRESS")

        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": response.data["results"][0]["id"],
                    "status_display": "in progress",
                    "title": "ToDo Test 001",
                    "description": "testing response A",
                }
            ],
        }

        actual_results = response.data["results"]
        for result in actual_results:
            result.pop("created_at", None)
            result.pop("updated_at", None)

        expected_results = expected_response["results"]

        self.assertEqual(actual_results, expected_results)
        self.assertEqual(response.data, expected_response)

    def test_response_get_to_list_with_search_in_title_or_description(self):
        response = self.client.get(f"{self.list_url}?search=searching")

        expected_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": response.data["results"][0]["id"],
                    "status_display": "concluded",
                    "title": "ToDo Test 002",
                    "description": "testing response B searching",
                },
                {
                    "id": response.data["results"][1]["id"],
                    "status_display": "concluded",
                    "title": "ToDo Test 003 searching",
                    "description": "testing response C",
                },
            ],
        }

        actual_results = response.data["results"]
        for result in actual_results:
            result.pop("created_at", None)
            result.pop("updated_at", None)

        expected_results = expected_response["results"]

        self.assertEqual(actual_results, expected_results)
        self.assertEqual(response.data, expected_response)

    def test_response_get_to_list_todo_by_id(self):
        todo_data = {
            "title": "ToDo Test 004",
            "description": "testing response D",
        }
        created_todo = self.client.post(self.list_url, todo_data, format="json")
        todo_id = created_todo.data["id"]

        response = self.client.get(f"{self.list_url}/{todo_id}")
        expected_data = {
            "id": todo_id,
            "status_display": "in progress",
            "title": "ToDo Test 004",
            "description": "testing response D",
        }

        response_data = response.data.copy()
        response_data.pop("created_at", None)
        response_data.pop("updated_at", None)

        self.assertEqual(response_data, expected_data)

    def test_response_get_to_list_todo_by_id_not_found(self):
        response = self.client.get(f"{self.list_url}/100")
        expected_data = {"detail": "Not found."}

        self.assertEqual(response.data, expected_data)

    def test_response_post_to_create_todo(self):
        todo_data = {"title": "ToDo Test", "description": "Testing response"}
        request_create = self.client.post(self.list_url, data=todo_data)
        todo_id = request_create.data["id"]

        expected_data = {
            "id": todo_id,
            "status_display": "in progress",
            "title": "ToDo Test",
            "description": "Testing response",
        }

        response_data = request_create.data.copy()
        response_data.pop("created_at", None)
        response_data.pop("updated_at", None)

        self.assertEqual(response_data, expected_data)

    def test_response_post_to_create_todo_with_invalid_status(self):
        todo_data = {"title": "ToDo Test", "status": "status"}
        request_create = self.client.post(self.list_url, data=todo_data)

        expected_data = {
            "error": "Invalid status value! Allowed values are: IN_PROGRESS, CONCLUDED"
        }

        self.assertEqual(request_create.data, expected_data)

    def test_response_patch_to_update_todo(self):
        todo_data = {"title": "ToDo Test", "description": "Testing response"}
        request_create = self.client.post(self.list_url, data=todo_data)
        todo_id = request_create.data["id"]

        todo_update = {"status": "CONCLUDED"}
        self.client.patch(f"{self.list_url}/{todo_id}", data=todo_update)

        updated_todo = self.client.get(f"{self.list_url}/{todo_id}").data

        expected_data = {
            "id": todo_id,
            "status_display": "concluded",
            "title": "ToDo Test",
            "description": "Testing response",
        }

        updated_todo.pop("created_at", None)
        updated_todo.pop("updated_at", None)

        self.assertEqual(updated_todo, expected_data)

    def test_response_patch_to_update_todo_with_invalid_status(self):
        todo_data = {"title": "ToDo Test", "description": "Testing response"}
        request_create = self.client.post(self.list_url, data=todo_data)
        todo_id = request_create.data["id"]

        todo_update = self.client.patch(
            f"{self.list_url}/{todo_id}", data={"status": "status"}
        )

        expected_data = {
            "error": "Invalid status value! Allowed values are: IN_PROGRESS, CONCLUDED"
        }

        self.assertEqual(todo_update.data, expected_data)

    def test_response_delete_to_delete_todo(self):
        todo_data = {
            "title": "ToDo Test 004",
            "description": "testing response D",
        }
        created_todo = self.client.post(self.list_url, todo_data, format="json")
        todo_id = created_todo.data["id"]

        response = self.client.delete(f"{self.list_url}/{todo_id}")
        self.assertEqual(response.data, None)

    def test_setup_creates_todos(self):
        self.assertEqual(models.ToDo.objects.count(), len(self.todos_data))

    def test_list_api_returns_all_todos(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], models.ToDo.objects.count())
