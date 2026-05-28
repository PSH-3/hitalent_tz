import pytest
from employees.models import Employee
from departments.services import create_department


@pytest.mark.django_db
def test_create_employee():
    dept = create_department(name="Backend")

    employee = Employee.objects.create(
        department=dept,
        full_name="John Doe",
        position="Developer",
    )

    assert employee.id is not None
    assert employee.department == dept