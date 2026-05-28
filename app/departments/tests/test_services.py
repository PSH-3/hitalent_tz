import pytest
from departments.services import create_department, move_department
from departments.models import Department


@pytest.mark.django_db
def test_create_department():
    dept = create_department(name="Backend")

    assert dept.id is not None
    assert dept.name == "Backend"


@pytest.mark.django_db
def test_cycle_prevention():
    a = create_department(name="A")
    b = create_department(name="B", parent_id=a.id)

    # попытка сделать A дочерним B → цикл
    with pytest.raises(Exception):
        move_department(department_id=a.id, parent_id=b.id)