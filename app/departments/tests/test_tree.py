import pytest
from departments.services import create_department, build_department_tree


@pytest.mark.django_db
def test_tree_depth_limit():
    root = create_department(name="Root")
    child = create_department(name="Child", parent_id=root.id)
    create_department(name="GrandChild", parent_id=child.id)

    tree = build_department_tree(root, depth=1)

    assert len(tree) > 0
    assert tree[0]["children"] == []