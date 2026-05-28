import pytest
from departments.services import create_department, delete_department
from departments.models import Department
from employees.models import Employee


@pytest.mark.django_db
def test_delete_cascade():
    dept = create_department(name="Backend")

    delete_department(
        department_id=dept.id,
        mode="cascade",
    )

    assert not Department.objects.filter(id=dept.id).exists()


@pytest.mark.django_db
def test_delete_reassign():
    a = create_department(name="A")
    b = create_department(name="B")

    emp = Employee.objects.create(
        department=a,
        full_name="John",
        position="Dev",
    )

    delete_department(
        department_id=a.id,
        mode="reassign",
        reassign_to_department_id=b.id,
    )

    emp.refresh_from_db()
    assert emp.department == b