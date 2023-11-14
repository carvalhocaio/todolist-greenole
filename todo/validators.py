from rest_framework import serializers

from todo import models


def status_validator(status):
    if status not in dict(models.ToDo.STATUS_CHOICES):
        allowed_values = [choice[0] for choice in models.ToDo.STATUS_CHOICES]
        raise serializers.ValidationError(
            {
                "error": f"Invalid status value! Allowed values are: {', '.join(allowed_values)}"
            }
        )
