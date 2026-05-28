from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "parent",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name cannot be empty")

        if len(value) > 200:
            raise serializers.ValidationError("Max length is 200")

        return value
    

class DepartmentTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "created_at",
            "children",
            "employees",
        ]

    def get_children(self, obj):
        depth = self.context.get("depth", 1)

        if depth <= 0:
            return []

        return DepartmentTreeSerializer(
            obj.children.all(),
            many=True,
            context={"depth": depth - 1},
        ).data

    def get_employees(self, obj):
        include = self.context.get("include_employees", True)

        if not include:
            return []

        from employees.serializers import EmployeeSerializer

        return EmployeeSerializer(obj.employees.all(), many=True).data