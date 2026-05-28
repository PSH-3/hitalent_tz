from .models import Department


def get_department(department_id: int) -> Department:
    return Department.objects.get(id=department_id)


def get_children(department: Department):
    return Department.objects.filter(parent=department).order_by("name")


def get_tree(department: Department, depth: int = 1):
    if depth < 0:
        return []

    children = get_children(department)

    return [
        {
            "id": child.id,
            "name": child.name,
            "created_at": child.created_at,
            "children": get_tree(child, depth - 1),
        }
        for child in children
    ]