from django.contrib import admin
from todo.models import ToDo


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at", "updated_at")
    list_display_links = ("title",)
    list_filter = ("status",)
    list_editable = ("status",)
    list_per_page = 20