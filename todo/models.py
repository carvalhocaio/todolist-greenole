from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ToDo(BaseModel):
    STATUS_CHOICES = (
        ("IN_PROGRESS", "in progress"),
        ("CONCLUDED", "concluded"),
    )

    title = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICES, default="IN_PROGRESS", blank=False, null=False
    )

    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDos"

    def __str__(self) -> str:
        return self.title
