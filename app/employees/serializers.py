from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "department",
            "full_name",
            "position",
            "hired_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Full name cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Max length is 200")
        return value

    def validate_position(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Position cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Max length is 200")
        return value