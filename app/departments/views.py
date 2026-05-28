from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import (
    create_department,
    move_department,
    delete_department,
)
from .selectors import get_department
from .serializers import DepartmentSerializer, DepartmentTreeSerializer
from .validators.depth import validate_depth


class DepartmentCreateView(APIView):
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        department = create_department(
            name=serializer.validated_data["name"],
            parent_id=serializer.validated_data.get("parent"),
        )

        return Response(
            DepartmentSerializer(department).data,
            status=status.HTTP_201_CREATED,
        )
    

class DepartmentDetailView(APIView):
    def get(self, request, id: int):
        depth = validate_depth(int(request.query_params.get("depth", 1)))
        include_employees = request.query_params.get("include_employees", "true") == "true"

        department = get_department(id)

        serializer = DepartmentTreeSerializer(
            department,
            context={
                "depth": depth,
                "include_employees": include_employees,
            },
        )

        return Response(serializer.data)
    

class DepartmentMoveView(APIView):
    def patch(self, request, id: int):
        new_parent_id = request.data.get("parent_id")

        department = move_department(
            department_id=id,
            parent_id=new_parent_id,
        )

        return Response(
            DepartmentSerializer(department).data
        )
    

class DepartmentDeleteView(APIView):
    def delete(self, request, id: int):
        mode = request.query_params.get("mode", "cascade")
        reassign_to = request.query_params.get("reassign_to_department_id")

        delete_department(
            department_id=id,
            mode=mode,
            reassign_to_department_id=reassign_to,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


