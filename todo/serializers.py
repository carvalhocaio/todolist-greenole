from rest_framework import serializers

from todo import models


class ToDoSerializer(serializers.ModelSerializer):
    status_value = serializers.CharField(source="get_status_display", read_only=True)
    status = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = models.ToDo
        fields = "__all__"

    def create(self, validated_data):
        validated_data["status"] = validated_data.get("status", "IN_PROGRESS")
        return models.ToDo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)

        new_status = validated_data.get("status", instance.status)
        if new_status not in dict(models.ToDo.STATUS_CHOICES):
            allowed_values = [choice[0] for choice in models.ToDo.STATUS_CHOICES]
            raise serializers.ValidationError(
                {
                    "error": f"Invalid status value! Allowed values are: {', '.join(allowed_values)}"
                }
            )
        instance.status = new_status

        instance.save()
        return instance
