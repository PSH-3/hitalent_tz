from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Department
from .selectors import get_department, get_children


@transaction.atomic
def create_department(*, name: str, parent_id: int | None = None) -> Department:
    if not name or not name.strip():
        raise ValidationError("Name cannot be empty")

    parent = None
    if parent_id:
        parent = get_department(parent_id)

    department = Department(name=name, parent=parent)
    department.full_clean()
    department.save()

    return department


@transaction.atomic
def move_department(*, department_id: int, parent_id: int | None):
    department = get_department(department_id)

    if parent_id:
        new_parent = get_department(parent_id)
    else:
        new_parent = None

    if new_parent and new_parent.id == department.id:
        raise ValidationError("Cannot set self as parent")

    current = new_parent
    while current:
        if current.id == department.id:
            raise ValidationError("Cycle detected in department tree")
        current = current.parent

    department.parent = new_parent
    department.full_clean()
    department.save()

    return department


def build_department_tree(department: Department, depth: int):
    if depth <= 0:
        return []
    
    children = get_children(department)

    return [
        {
            "id": child.id,
            "name": child.name,
            "children": build_department_tree(child, depth - 1),
        }
        for child in children
    ]


@transaction.atomic
def delete_department(
    *,
    department_id: int,
    mode: str,
    reassign_to_department_id: int | None = None,
):
    if mode not in {"cascade", "reassign"}:
        raise ValidationError("Invalid mode")
    
    department = get_department(department_id)

    if mode == "cascade":
        department.delete()
        return

    else:
        if not reassign_to_department_id:
            raise ValidationError("reassign_to_department_id is required")

        if reassign_to_department_id == department.id:
            raise ValidationError("Cannot reassign to self")

        target = get_department(reassign_to_department_id)

        department.employees.update(department=target)
        department.delete()
