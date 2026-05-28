from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.serializers import EmployeeSerializer
from employees.models import Employee
from ..departments.selectors import get_department


class DepartmentEmployeeCreateView(APIView):
    def post(self, request, id: int):
        department = get_department(id)

        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee = Employee.objects.create(
            department=department,
            **serializer.validated_data,
        )

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_201_CREATED,
        )