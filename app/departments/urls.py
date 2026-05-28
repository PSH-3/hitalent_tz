from django.urls import path

from .views import (
    DepartmentCreateView,
    DepartmentDetailView,
    DepartmentMoveView,
    DepartmentDeleteView,
)
from ..employees.views import DepartmentEmployeeCreateView

app_name = 'departments'

urlpatterns = [
    path(
        "departments/",
        DepartmentCreateView.as_view(),
        name="department-create",
    ),

    path(
        "departments/<int:id>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),

    path(
        "departments/<int:id>/move/",
        DepartmentMoveView.as_view(),
        name="department-move",
    ),

    path(
        "departments/<int:id>/delete/",
        DepartmentDeleteView.as_view(),
        name="department-delete",
    ),
    path(
        "departments/<int:id>/employees/",
        DepartmentEmployeeCreateView.as_view(),
        name="department-employee-create",
    ),
]