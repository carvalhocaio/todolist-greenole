from rest_framework import serializers

from todo import models, validators


class ToDoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    status = serializers.CharField(
        required=False,
        write_only=True,
        help_text="Status of the ToDo (IN_PROGRESS by default)",
    )

    class Meta:
        model = models.ToDo
        fields = "__all__"

    def create(self, validated_data):
        if "status" in validated_data:
            validators.status_validator(validated_data["status"])

        validated_data["status"] = validated_data.get("status", "IN_PROGRESS")
        return models.ToDo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)

        new_status = validated_data.get("status", instance.status)
        validators.status_validator(new_status)
        instance.status = new_status

        instance.save()
        return instance
